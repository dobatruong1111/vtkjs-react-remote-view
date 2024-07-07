import { useState, useRef, useEffect, useCallback } from "react";

import wslink from "./wslink";

import logo from "./assets/logo.png";

import "./App.css";

import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Slider,
  IconButton,
  LinearProgress,
} from "@mui/material";
import { CameraAlt } from "@mui/icons-material";
import RemoteRenderView from "./RemoteRenderingView";
import axios from "axios";

function App() {
  const context = useRef({});
  // const [resolution, setResolution] = useState(6);
  const [client, setClient] = useState(null);
  const [busy, setBusy] = useState(0);

  console.log("re-render");

  useEffect(() => {
    console.log("before fetch data");
    axios.post("http://localhost:8888/ws/rest/v1/session3d/websocketlink",
      {
        sessionID: "38ad3379-12bc-49a9-937e-c29cc78e9295",
        studyUID: "1.3.12.2.1107.5.1.4.66827.30000023041823414870500000493",
        seriesUID: "1.3.12.2.1107.5.1.4.66827.30000023041823425238300068850"
      }
    ).then(function (response) {
      let wsURL = response.data?.websocketUrl;
      if (wsURL) {
        console.log("after fetch data");
        wslink.connect(context.current, setClient, setBusy, wsURL);
      }
    }).catch(function (error) {
      console.log("error: ", error);
    })

    // const wsURL = "ws://localhost:1234/ws";
    // wslink.connect(context.current, setClient, setBusy, wsURL);
  }, []);

  // const updateResolution = (_event, newResolution) => {
  //   setResolution(newResolution);
  //   wslink.updateResolution(context.current, newResolution);
  // };

  const resetCamera = () => {
    wslink.resetCamera(context.current);
  }

  const applyBonePresetCT = () => {
    wslink.applyBonePresetCT(context.current);
  }

  const applyAngioPresetCT = () => {
    wslink.applyAngioPresetCT(context.current);
  }

  const applyMusclePresetCT = () => {
    wslink.applyMusclePresetCT(context.current);
  }

  const applyMipPresetCT = () => {
    wslink.applyMipPresetCT(context.current);
  }

  const activeLength = () => {
    wslink.activeLength(context.current);
  }

  const activeAngle = () => {
    wslink.activeAngle(context.current);
  }

  const activeCut = () => {
    wslink.activeCut(context.current);
  }

  const activeCutFreehand = () => {
    wslink.activeCutFreehand(context.current);
  }

  const activePan = () => {
    wslink.activePan(context.current);
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="inherit">
        <Toolbar>
          <img src={logo} alt="logo" className="logo"></img>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            3D Viewer
          </Typography>
          <IconButton onClick={applyBonePresetCT}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={applyAngioPresetCT}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={applyMusclePresetCT}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={applyMipPresetCT}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={activeLength}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={activeAngle}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={activeCut}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={activeCutFreehand}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={activePan}>
            <CameraAlt />
          </IconButton>
          <IconButton onClick={resetCamera}>
            <CameraAlt />
          </IconButton>
        </Toolbar>
        <LinearProgress sx={{ opacity: !!busy ? 1 : 0 }} />
      </AppBar>

      <Box className="appContent">
        <div style={{ position: "relative", width: "100%", height: "100%" }}>
          <RemoteRenderView client={client} />
        </div>
      </Box>
    </Box>
  );
}

export default App;
