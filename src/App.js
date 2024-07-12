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
  Button,
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
    axios.post("http://192.168.1.13:8888/ws/rest/v1/session3d/websocketlink",
      {
        session2D: "5e6395d2-ea80-481d-a593-89e37ddec0e2",
        studyUID: "2.25.291093576543455631656845608426318550200",
        seriesUID: "1.3.12.2.1107.5.1.4.96556.30000024032808413061600012199"
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
          <Button variant="outlined" onClick={applyBonePresetCT}>Bone</Button>
          <Button variant="outlined" onClick={applyAngioPresetCT}>Angio</Button>
          <Button variant="outlined" onClick={applyMusclePresetCT}>Muscle</Button>
          <Button variant="outlined" onClick={applyMipPresetCT}>Mip</Button>
          <Button variant="outlined" onClick={activeLength}>Length</Button>
          <Button variant="outlined" onClick={activeAngle}>Angle</Button>
          <Button variant="outlined" onClick={activeCut}>Cut</Button>
          <Button variant="outlined" onClick={activeCutFreehand}>Freehand</Button>
          <Button variant="outlined" onClick={activePan}>Pan</Button>
          <Button variant="outlined" onClick={resetCamera}>Reset</Button>
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
