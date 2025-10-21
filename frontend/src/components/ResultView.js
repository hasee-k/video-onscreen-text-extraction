// src/components/ResultView.js
import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Typography,
} from "@mui/material";
import { useRef } from "react";

export default function ResultView({ preview, result }) {
  const detailed = result?.detailed_extraction ?? [];
  const videoRef = useRef(null);

  const handleNavigateVideoTimestamp = (timestamp) => {
    const video = videoRef.current;
    if (!video || !timestamp) return;

    // Convert "HH:MM:SS" → seconds
    const parts = timestamp.split(":").map(Number);
    if (parts.length !== 3 || parts.some(isNaN)) {
      console.warn("Invalid timestamp:", timestamp);
      return;
    }

    const [hours, minutes, seconds] = parts;
    const timeInSeconds = hours * 3600 + minutes * 60 + seconds;

    if (!isFinite(timeInSeconds)) return;

    const seek = () => {
      video.currentTime = timeInSeconds;
      video.play();
    };

    if (video.readyState >= 1) {
      seek();
    } else {
      video.addEventListener("loadedmetadata", seek, { once: true });
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 3,
        alignItems: "flex-start",
        flexWrap: "wrap",
      }}
    >
      {/* Left column: Video preview */}
      <Box sx={{ flex: 1, minWidth: "45%" }}>
        {preview ? (
          <video
            ref={videoRef}
            src={preview}
            controls
            style={{
              width: "100%",
              borderRadius: "10px",
              boxShadow: "0 0 15px rgba(0,0,0,0.3)",
            }}
          />
        ) : (
          <Typography>No video preview available.</Typography>
        )}
      </Box>

      {/* Right column: Extraction details */}
      <Box
        sx={{
          flex: 1,
          backgroundColor: "#fafafa",
          padding: 2,
          borderRadius: 2,
          boxShadow: "0 0 10px rgba(0,0,0,0.15)",
          maxHeight: "500px",
          overflowY: "auto",
          minWidth: "45%",
        }}
      >
        <Typography variant="h6" gutterBottom sx={{ fontWeight: "bold" }}>
          🧾 Detailed Frame Extraction
        </Typography>
        <Divider sx={{ mb: 2 }} />

        {detailed.map((entry, idx) => (
          <Card
            key={idx}
            sx={{
              mb: 2,
              backgroundColor: "#e3f2fd",
              borderRadius: 2,
              boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
            }}
          >
            <CardContent>
              <Typography variant="subtitle1" sx={{ fontWeight: "bold" }}>
                Frame {idx + 1}
              </Typography>

              {/* Timestamp */}
              {entry.time_stamp && (
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ mb: 1 }}
                >
                  <Button
                    variant="text"
                    onClick={() =>
                      handleNavigateVideoTimestamp(entry.time_stamp)
                    }
                  >
                    🕒 Timestamp: {entry.time_stamp}
                  </Button>
                </Typography>
              )}

              {/* Extracted text */}
              <Typography sx={{ mb: 1 }}>
                <strong>📝 Extracted Text:</strong>{" "}
                {entry.text ? (
                  <span style={{ color: "#2e7d32" }}>{entry.text}</span>
                ) : (
                  <span style={{ color: "gray" }}>No text detected</span>
                )}
              </Typography>

              {/* Frame description */}
              <Typography sx={{ mb: 1 }}>
                <strong>🎞️ Frame Description:</strong>{" "}
                {entry.image_description ? (
                  <span style={{ color: "#1565c0" }}>
                    {entry.image_description}
                  </span>
                ) : (
                  <span style={{ color: "gray" }}>N/A</span>
                )}
              </Typography>

              {/* 🖼️ Frame image preview */}
              {entry.image && (
                <Box
                  component="img"
                  src={`data:image/jpeg;base64,${entry.image}`}
                  alt={`Frame ${idx + 1}`}
                  sx={{
                    width: "100%",
                    maxHeight: "300px",
                    objectFit: "contain",
                    borderRadius: 1,
                    mt: 1,
                  }}
                />
              )}
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
}
