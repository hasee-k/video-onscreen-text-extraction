# frontend_router.py
import uuid
import json
import sys
import subprocess
import threading
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse

router = APIRouter()
JOBS_ROOT = Path("jobs")
JOBS_ROOT.mkdir(exist_ok=True)

# in-memory job store (persisted results saved under jobs/<job_id>/result.json)
jobs = {}

@router.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    # create job id & folder
    job_id = str(uuid.uuid4())
    job_dir = JOBS_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    # save uploaded file
    video_path = job_dir / file.filename
    with open(video_path, "wb") as f:
        content = await file.read()
        f.write(content)

    jobs[job_id] = {"status": "queued", "result": None, "error": None}

    # launch extraction in background thread (subprocess)
    def run_job():
        try:
            jobs[job_id]["status"] = "processing"
            # call run_extraction.py using the same python executable
            proc = subprocess.Popen(
                [sys.executable, "run_extraction.py", "--video", str(video_path), "--output", str(job_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            out, err = proc.communicate()
            if proc.returncode != 0:
                jobs[job_id]["status"] = "failed"
                jobs[job_id]["error"] = err.decode(errors="replace")
                return

            # prefer reading result.json file if present
            result_file = job_dir / "result.json"
            if result_file.exists():
                with open(result_file, "r", encoding="utf-8") as rf:
                    result = json.load(rf)
            else:
                # else try decode stdout
                try:
                    result = json.loads(out.decode())
                except Exception:
                    result = {"stdout": out.decode(errors="replace"), "stderr": err.decode(errors="replace")}
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = result
            # store result on disk
            with open(job_dir / "result.json", "w", encoding="utf-8") as rf:
                json.dump(result, rf, ensure_ascii=False, indent=2)
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)

    threading.Thread(target=run_job, daemon=True).start()

    return JSONResponse({"job_id": job_id, "status": "queued"}, status_code=201)


@router.get("/api/status/{job_id}")
def job_status(job_id: str):
    j = jobs.get(job_id)
    if not j:
        raise HTTPException(status_code=404, detail="job not found")
    return {"job_id": job_id, "status": j["status"], "error": j.get("error")}


@router.get("/api/result/{job_id}")
def job_result(job_id: str):
    j = jobs.get(job_id)
    if not j:
        raise HTTPException(status_code=404, detail="job not found")
    if j["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"job status is {j['status']}")
    return j["result"]


@router.get("/api/download/{job_id}/{filename}")
def download_file(job_id: str, filename: str):
    job_dir = JOBS_ROOT / job_id
    file_path = job_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(file_path, filename=filename)
