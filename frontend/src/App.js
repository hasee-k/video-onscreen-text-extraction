// App.js
import React, { useState, useMemo } from "react";
import VideoUpload from "./components/VideoUpload";
import "./App.css";

import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  CssBaseline,
  Container,
  Box,
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  // --- Themes ---
  const theme = useMemo(
    () =>
      createTheme({
        palette: { mode: darkMode ? "dark" : "light" },
      }),
    [darkMode]
  );

  const appBarColor = darkMode ? "#b39ddb" : "#9c27b0";

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* Top AppBar */}
      <AppBar position="static" sx={{ backgroundColor: appBarColor }}>
        <Toolbar sx={{ justifyContent: "space-between",minHeight: 600, px: 3,}}>
           
          <Box sx={{ flex: 1, textAlign: "center" }}>
            <Typography
              variant="h4"
              component="div"
              sx={{ fontWeight: "bold", fontSize: "2.2rem", letterSpacing: 1 }}
            >
              🎥 Video On-screen Text
            </Typography>
          </Box>
          <IconButton color="inherit" onClick={() => setDarkMode(!darkMode)}>
            {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-start",
          textAlign: "center",
          background: "linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab)",
          backgroundSize: "400% 400%",
          animation: "gradientBG 15s ease infinite",
          py: 8, // extra padding top/bottom
        }}
      >
        <Container
          sx={{
            width: "100%",
            maxWidth: 900, // increased main container width
            backgroundColor: darkMode ? "rgba(0,0,0,0.4)" : "rgba(255,255,255,0.6)",
            borderRadius: 4,
            p: 4,
            boxShadow: 6,
          }}
        >
          <Typography
            variant="h5"
            gutterBottom
            sx={{ color: theme.palette.text.primary, mb: 4, fontWeight: "bold" }}
          >
            Upload a video, wait for extraction, and view/download results.
          </Typography>

          {/* Add figure/illustration */}
          <Box sx={{ mb: 4 }}>
            <img
              src="https://cdn-icons-png.flaticon.com/512/3039/3039471.png" // example figure
              alt="Video Illustration"
              width="150"
              style={{ opacity: 0.8 }}
            />
          </Box>

          <VideoUpload darkMode={darkMode} />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
