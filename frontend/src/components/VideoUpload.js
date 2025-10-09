// src/components/VideoUpload.js
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  Button,
  LinearProgress,
  Typography,
  Card,
  CardContent,
  CardActions,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import VisibilityIcon from "@mui/icons-material/Visibility";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DownloadIcon from "@mui/icons-material/Download";
import { useTheme } from "@mui/material/styles";

export default function VideoUpload({ darkMode }) {
  const theme = useTheme();

  // --- Favorite colors ---
  const myButtonColor = "#ff5722"; // deep orange
  const myButtonHover = "#6f3726ff"; // darker orange
  const mySecondaryColor = "#4caf50"; // green
  const myProgressBg = "#cfd8dc"; // light grey
  const myProgressBar = "#ff9800"; // amber
  const mySnackbarBgLight = "#f5f5f5";
  const mySnackbarBgDark = "#ec74e4ff";

  // --- Card Colors by Theme ---
  const cardBg = darkMode ? "#bfe632ff" : "#4fde3fff"; // light blue for dark, cyan for light

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploadPct, setUploadPct] = useState(0);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);

  // Snackbar state
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "info",
  });

  const pollRef = useRef(null);

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [preview]);

  const onFileChange = (e) => {
    const f = e.target.files[0];
    setFile(f);
    if (f) setPreview(URL.createObjectURL(f));
    setSnackbar({
      open: true,
      message: `Selected file: ${f?.name}`,
      severity: "info",
    });
  };

  const deleteVideo = () => {
    setFile(null);
    setPreview(null);
    setUploadPct(0);
    setJobId(null);
    setStatus(null);
    setResult(null);
    if (pollRef.current) clearInterval(pollRef.current);
    setSnackbar({
      open: true,
      message: "Video deleted successfully.",
      severity: "warning",
    });
  };

  // ---- Upload Handler with dynamic progress snackbar ----
  const handleUpload = async () => {
    if (!file) {
      setSnackbar({
        open: true,
        message: "Please choose a video first.",
        severity: "error",
      });
      return;
    }

    setUploadPct(0);
    setJobId(null);
    setStatus(null);
    setResult(null);
    setSnackbar({ open: true, message: "Starting upload...", severity: "info" });

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/api/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (ev) => {
          const pct = Math.round((ev.loaded / ev.total) * 100);
          setUploadPct(pct);
          setSnackbar({ open: true, message: `Uploading ${pct}%...`, severity: "info" });
        },
      });

      setJobId(res.data.job_id);
      setStatus(res.data.status || "queued");
      setSnackbar({ open: true, message: "Upload successful! Processing started...", severity: "success" });

      pollRef.current = setInterval(async () => {
        try {
          const s = await axios.get(`http://localhost:8000/api/status/${res.data.job_id}`);
          setStatus(s.data.status);

          if (s.data.status === "completed") {
            clearInterval(pollRef.current);
            const r = await axios.get(`http://localhost:8000/api/result/${res.data.job_id}`);
            setResult(r.data);
            setSnackbar({ open: true, message: "Processing completed! 🎉", severity: "success" });
          } else if (s.data.status === "failed") {
            clearInterval(pollRef.current);
            const r = await axios.get(`http://localhost:8000/api/result/${res.data.job_id}`).catch(() => null);
            setResult({ error: s.data.error || (r && r.data) || "Processing failed." });
            setSnackbar({ open: true, message: "Processing failed ❌", severity: "error" });
          }
        } catch (err) {
          console.error("Polling error", err);
          setSnackbar({ open: true, message: "Polling error. Please retry.", severity: "error" });
        }
      }, 2000);
    } catch (err) {
      console.error(err);
      setSnackbar({ open: true, message: "Upload failed. Open console for details.", severity: "error" });
    }
  };

  const downloadResult = () => {
    if (!result || !jobId) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `result_${jobId}.json`;
    a.click();
    URL.revokeObjectURL(url);
    setSnackbar({ open: true, message: "Result downloaded as JSON ✅", severity: "success" });
  };

  
  return (
    <>
      <Card sx={{ maxWidth: 650, mx: "auto", mt: 4, backgroundColor: cardBg }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: "bold" }}>
            📽️ Video Text Extraction
          </Typography>

          <Button
            variant="contained"
            component="label"
            startIcon={<CloudUploadIcon />}
            sx={{
              backgroundColor: myButtonColor,
              color: theme.palette.getContrastText(myButtonColor),
              "&:hover": { backgroundColor: myButtonHover },
              mt: 1,
            }}
          >
            Select Video
            <input type="file" hidden accept="video/*" onChange={onFileChange} />
          </Button>

          {file && <Typography variant="body2" sx={{ mt: 1 }}>Selected: {file.name}</Typography>}

          {preview && (
            <div style={{ marginTop: 12 }}>
              <video src={preview} controls width="100%" />
            </div>
          )}

          {uploadPct > 0 && uploadPct < 100 && (
            <LinearProgress
              variant="determinate"
              value={uploadPct}
              sx={{
                mt: 2,
                backgroundColor: theme.palette.mode === "dark" ? "#333" : myProgressBg,
                "& .MuiLinearProgress-bar": { backgroundColor: myProgressBar },
              }}
            />
          )}

          {jobId && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              Job ID: <b>{jobId}</b> — Status: {status}
            </Typography>
          )}
        </CardContent>

        {/* --- Updated CardActions --- */}
        <CardActions sx={{ justifyContent: "space-between", px: 2, pb: 2 }}>
          {/* Show Upload & Extract only if a file is selected */}
          {file && (
            <Button
              variant="contained"
              onClick={handleUpload}
              sx={{
                backgroundColor: myButtonColor,
                color: theme.palette.getContrastText(myButtonColor),
                "&:hover": { backgroundColor: myButtonHover },
              }}
            >
              Upload & Extract
            </Button>
          )}

          {file && (
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={deleteVideo}
            >
              Delete Video
            </Button>
          )}
        </CardActions>

        {result && (
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: "bold" }}>
              Extraction Result
            </Typography>
            <Button
              variant="outlined"
              startIcon={<VisibilityIcon />}
              onClick={() => setOpenDialog(true)}
              sx={{ mr: 2 }}
            >
              View
            </Button>
            <Button
              variant="contained"
              sx={{ backgroundColor: mySecondaryColor, color: theme.palette.getContrastText(mySecondaryColor) }}
              startIcon={<DownloadIcon />}
              onClick={downloadResult}
            >
              Download JSON
            </Button>
          </CardContent>
        )}

        <Dialog
          open={openDialog}
          onClose={() => setOpenDialog(false)}
          maxWidth="md"
          fullWidth
          PaperProps={{ sx: { backgroundColor: cardBg } }}
        >
          <DialogTitle sx={{ fontWeight: "bold" }}>Extraction Result</DialogTitle>
          <DialogContent dividers>
            {result?.extracted_text ? (
              <ul>
                {result.extracted_text.map((line, idx) => (
                  <li key={idx}>{line}</li>
                ))}
              </ul>
            ) : (
              <Typography color="error">{result?.error || "No extracted text available."}</Typography>
            )}
            {result?.frame_count && <Typography sx={{ mt: 1 }}>Frames Processed: {result.frame_count}</Typography>}
            {result?.processing_time && <Typography>Processing Time: {result.processing_time}s</Typography>}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      </Card>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{
            width: "100%",
            backgroundColor: darkMode ? mySnackbarBgDark : mySnackbarBgLight,
            color: theme.palette.text.primary,
          }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
}
