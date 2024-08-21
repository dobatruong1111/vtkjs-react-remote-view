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
    // axios.post("https://viewer.saolasoft.vn/ws/rest/v1/session3d/websocketlink",
    //   {
    //     session2D: "1475c1a9-cac3-42f1-b96f-a62e9aa9ad11",
    //     studyUID: "1.2.840.113619.2.415.3.2831155460.530.1721039812.497",
    //     seriesUID: "1.2.840.113619.2.415.3.2831155460.530.1721039812.503.3"
    //   }
    // ).then(function (response) {
    //   let wsURL = response.data?.websocketUrl;
    //   if (wsURL) {
    //     let temp = `wss://viewer.saolasoft.vn${wsURL}`;
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

  const rotateDirection = (direction) => {
    wslink.rotateDirection(context.current, direction)
  }

  const deleteAll = () => {
    wslink.delete(context.current);
  }

  const shading = () => {
    wslink.shading(context.current);
  }

  const reinitializeServer = (seriesUID) => {
    wslink.reinitializeServer(context.current, seriesUID);
  }

  const applyPreset = (name) => {
    wslink.applyPreset(context.current, name);
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

  const shift = () => {
    wslink.shift(context.current);
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="inherit">
        <Toolbar>
          <img src={logo} alt="logo" className="logo"></img>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            3D Viewer
          </Typography>
          {/* <Button variant="outlined" onClick={() => reinitializeServer("1.2.840.113619.2.415.3.2831155460.530.1721039812.503")}>Create</Button> */}
          <Button variant="outlined" onClick={shift}>Shift</Button>
          <Button variant="outlined" onClick={activeRotate}>Rotate</Button>
          {/* <Button variant="outlined" onClick={() => rotateDirection("ANTERIOR")}>A</Button>
          <Button variant="outlined" onClick={() => rotateDirection("POSTERIOR")}>P</Button>
          <Button variant="outlined" onClick={() => rotateDirection("LEFT")}>L</Button>
          <Button variant="outlined" onClick={() => rotateDirection("RIGHT")}>R</Button>
          <Button variant="outlined" onClick={() => rotateDirection("SUPERIOR")}>S</Button>
          <Button variant="outlined" onClick={() => rotateDirection("INFERIOR")}>I</Button> */}
          <Button variant="outlined" onClick={() => applyPreset("CT-AAA")}>CT-AAA</Button>
          <Button variant="outlined" onClick={() => applyPreset("CT-Cardiac")}>CT-Cardiac</Button>
          <Button variant="outlined" onClick={() => applyPreset("CT-Bone")}>CT-Bone</Button>
          <Button variant="outlined" onClick={() => applyPreset("CT-Chest-Vessels")}>CT-Chest-Vessels</Button>
          {/* <Button variant="outlined" onClick={() => applyPreset("Standard")}>I-Standard</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("Soft + Skin")}>Soft + Skin</Button> */}
          {/* <Button variant="outlined" onClick={activeLength}>Length</Button> */}
          {/* <Button variant="outlined" onClick={activeAngle}>Angle</Button> */}
          {/* <Button variant="outlined" onClick={deleteAll}>delete</Button> */}
          <Button variant="outlined" onClick={activeCut}>Cut</Button>
          <Button variant="outlined" onClick={activeCutFreehand}>Freehand</Button>
          <Button variant="outlined" onClick={activePan}>Pan</Button>
          <Button variant="outlined" onClick={resetViewport}>Reset</Button>
          {/* <Button variant="outlined" onClick={shading}>Shading</Button> */}
        </Toolbar>
        <LinearProgress sx={{ opacity: !!busy ? 1 : 0 }} />
      </AppBar>

      <Box className="appContent">
        <div className="views">
          <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
            <RemoteRenderView client={client} viewId="1" />
          </div>
          {/* <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="2" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="3" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px" }}>
            <RemoteRenderView client={client} viewId="4" />
          </div> */}
        </div>
      </Box>
    </Box>
  );
}

export default App;
