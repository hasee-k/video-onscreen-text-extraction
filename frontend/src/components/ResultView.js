// src/components/ResultView.js
import React from "react";
import { Typography, Box, Card, CardContent, Divider } from "@mui/material";

export default function ResultView({ preview, result }) {
  const detailed = result?.detailed_extraction ?? [];

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

        {detailed.length > 0 ? (
          detailed.map((entry, idx) => (
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
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    🕒 Timestamp: {entry.time_stamp}
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

                {/* Image/scene description */}
                <Typography>
                  <strong>🎞️ Frame Description:</strong>{" "}
                  {entry.image_description ? (
                    <span style={{ color: "#1565c0" }}>{entry.image_description}</span>
                  ) : (
                    <span style={{ color: "gray" }}>N/A</span>
                  )}
                </Typography>
              </CardContent>
            </Card>
          ))
        ) : result?.extracted_text?.length > 0 ? (
          result.extracted_text.map((line, idx) => (
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
                <Typography>
                  <strong>📝 Extracted Text:</strong> {line || "No text detected"}
                </Typography>
              </CardContent>
            </Card>
          ))
        ) : (
          <Typography color="error">No extracted data available.</Typography>
        )}
      </Box>
    </Box>
  );
}
