from app.services.video_service import text_extractor_from_video
from fastapi import UploadFile
import aiofiles
import asyncio

async def extract_video(video_path: str, output_dir: str):
    """
    Connects to real video text extraction
    """
    # Simulate UploadFile for compatibility
    class DummyUploadFile:
        def __init__(self, filename):
            self.filename = filename
        async def read(self):
            async with aiofiles.open(filename, "rb") as f:
                return await f.read()

    dummy_file = DummyUploadFile(video_path)
    result = await text_extractor_from_video(dummy_file)

    # Convert Pydantic model -> dict if needed
    if hasattr(result, "dict"):
        result = result.dict()

    return result

def main():
    import argparse, json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # run async extractor
    result = asyncio.run(extract_video(args.video, str(out_dir)))

    # save + print
    with open(out_dir / "result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result))
