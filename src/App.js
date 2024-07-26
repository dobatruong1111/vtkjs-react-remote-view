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
    // console.log("before fetch data");
    // axios.post("http://192.168.1.13:9000/ws/rest/v1/session3d/websocketlink",
    //   {
    //     session2D: "874ee644-d16b-4c43-8cbe-3e95ce7d9f8d",
    //     studyUID: "1.2.840.113704.9.1000.16.0.20240527133901371",
    //     seriesUID: "1.2.840.113704.9.1000.16.1.2024052713392627100020002"
    //   }
    // ).then(function (response) {
    //   let wsURL = response.data?.websocketUrl;
    //   if (wsURL) {
    //     let temp = `ws://192.168.1.13:9000${wsURL}`;
    //     console.log("after fetch data");
    //     wslink.connect(context.current, setClient, setBusy, temp);
    //   }
    // }).catch(function (error) {
    //   console.log("error: ", error);
    // })

    const wsURL = "ws://localhost:1234/ws";
    wslink.connect(context.current, setClient, setBusy, wsURL);
  }, []);

  // const updateResolution = (_event, newResolution) => {
  //   setResolution(newResolution);
  //   wslink.updateResolution(context.current, newResolution);
  // };

  const applyPreset = () => {
    wslink.applyPreset(context.current);
  }

  const resetViewport = () => {
    wslink.resetViewport(context.current);
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

  const activeRotate = () => {
    wslink.activeRotate(context.current);
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="inherit">
        <Toolbar>
          <img src={logo} alt="logo" className="logo"></img>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            3D Viewer
          </Typography>
          <Button variant="outlined" onClick={activeRotate}>Rotate</Button>
          <Button variant="outlined" onClick={applyPreset}>Preset</Button>
          <Button variant="outlined" onClick={activeLength}>Length</Button>
          <Button variant="outlined" onClick={activeAngle}>Angle</Button>
          <Button variant="outlined" onClick={activeCut}>Cut</Button>
          <Button variant="outlined" onClick={activeCutFreehand}>Freehand</Button>
          <Button variant="outlined" onClick={activePan}>Pan</Button>
          <Button variant="outlined" onClick={resetViewport}>Reset</Button>
        </Toolbar>
        <LinearProgress sx={{ opacity: !!busy ? 1 : 0 }} />
      </AppBar>

      <Box className="appContent">
        <div className="views">
          <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="1" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="2" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="3" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="4" />
          </div>
        </div>
      </Box>
    </Box>
  );
}

export default App;
