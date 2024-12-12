import { useState, useRef, useEffect } from "react";

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

  // console.log("re-render");

  useEffect(() => {
    // axios.post("https://viewer.saolasoft.vn/ws/rest/v1/session3d/websocketlink",
    //   {
    //     session2D: "315d7a54-6710-4180-bc0a-d2e10764ce93",
    //     studyUID: "2.25.313472556869089568467430831702503378132",
    //     seriesUID: "1.2.840.113619.2.495.13407973.1393672.30831.1725321555.543"
    //   }
    // ).then(function (response) {
    //   let wsURL = response.data?.websocketUrl;
    //   if (wsURL) {
    //     let temp = `wss://viewer.saolasoft.vn${wsURL}`;
    //     wslink.connect(context.current, setClient, setBusy, temp);
    //   }
    // }).catch(function (error) {
    //   console.log("error: ", error);
    // })

    // axios.post("http://192.168.1.13:8888/ws/rest/v1/session3d/websocketlink",
    //   {
    //     session2D: "f49b2c32-0ee1-4986-9a8b-e3efa7e7145e",
    //     studyUID: "2.25.313472556869089568467430831702503378132",
    //     seriesUID: "1.2.840.113619.2.311.21069929483845356808000867488496312106"
    //   }
    // ).then(function (response) {
    //   let wsURL = response.data?.websocketUrl;
    //   if (wsURL) {
    //     let temp = `ws://192.168.1.13:8888${wsURL}`;
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

  const reinitializeServer = () => {
    wslink.reinitializeServer(context.current);
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

  const removeBed = () => {
    wslink.removeBed(context.current);
  }

  const activePan = () => {
    wslink.activePan(context.current);
  }

  const activeZoom = () => {
    wslink.activeZoom(context.current);
  }

  const activeRotate = () => {
    wslink.activeRotate(context.current);
  }

  const shift = () => {
    wslink.shift(context.current);
  }

  const dicomDownload = () => {
    wslink.dicomDownload(context.current, "1.2.840.113619.2.438.3.2831208971.408.1719531439.122", "1.2.840.113619.2.438.3.2831208971.408.1719531439.198")
  }

  const logStatus = () => {
    wslink.getStatus(context.current);

    context.current.client.getConnection().getSession().subscribe("wslink.channel", ([status]) => {
      console.log(status);
    });
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="inherit">
        <Toolbar>
          {/* <Button variant="outlined" onClick={reinitializeServer}>Download</Button>
          <Button variant="outlined" onClick={() => wslink.createVolume(context.current)}>Create</Button>
          <Button variant="outlined" onClick={shift}>WL</Button> */}
          {/* <Button variant="outlined" onClick={activeRotate}>Rotate</Button> */}
          {/* <Button variant="outlined" onClick={activeZoom}>Zoom</Button> */}
          {/* <Button variant="outlined" onClick={activePan}>Pan</Button> */}
          {/* <Button variant="outlined" onClick={() => rotateDirection("ANTERIOR")}>A</Button>
          <Button variant="outlined" onClick={() => rotateDirection("POSTERIOR")}>P</Button>
          <Button variant="outlined" onClick={() => rotateDirection("LEFT")}>L</Button>
          <Button variant="outlined" onClick={() => rotateDirection("RIGHT")}>R</Button>
          <Button variant="outlined" onClick={() => rotateDirection("SUPERIOR")}>S</Button>
          <Button variant="outlined" onClick={() => rotateDirection("INFERIOR")}>I</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("CT-AAA")}>CT-AAA</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("CT-Cardiac")}>CT-Cardiac</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("CT-Bone")}>CT-Bone</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("CT-Chest-Vessels")}>CT-Chest-Vessels</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("Standard")}>Standard</Button> */}
          {/* <Button variant="outlined" onClick={() => applyPreset("Soft + Skin")}>Soft + Skin</Button> */}
          {/* <Button variant="outlined" onClick={activeLength}>Length</Button> */}
          {/* <Button variant="outlined" onClick={activeAngle}>Angle</Button> */}
          {/* <Button variant="outlined" onClick={deleteAll}>delete</Button> */}
          {/* <Button variant="outlined" onClick={activeCut}>Crop</Button> */}
          {/* <Button variant="outlined" onClick={activeCutFreehand}>Freehand</Button> */}
          {/* <Button variant="outlined" onClick={removeBed}>Bed</Button> */}
          {/* <Button variant="outlined" onClick={resetViewport}>Reset</Button> */}
          {/* <Button variant="outlined" onClick={shading}>Shading</Button> */}
          {/* <Button variant="outlined" onClick={dicomDownload}>download</Button> */}
          {/* <Button variant="outlined" onClick={logStatus}>log status</Button> */}
          <Button variant="outlined" onClick={() => wslink.slice3D(context.current, ["AXIAL", "CORONAL", "SAGITAL"])}>Turn on</Button>
          <Button variant="outlined" onClick={() => wslink.slice3D(context.current, [])}>Turn off</Button>
          <Button variant="outlined" onClick={() => wslink.setCrosslines(context.current, [])}>Crosslines</Button>
          {/* <Button variant="outlined" onClick={() => wslink.slice3D(context.current, ["AXIAL", "CORONAL"])}>Test</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.flythrough(context.current, "PREV")}>Prev</Button>
          <Button variant="outlined" onClick={() => wslink.flythrough(context.current, "NEXT")}>Next</Button>
          <Button variant="outlined" onClick={() => wslink.flythrough(context.current, "REVERT")}>Revert</Button> */}
          <Button variant="outlined" onClick={() => wslink.resetViewport(context.current)}>Reset</Button>
          {/* <Button variant="outlined" onClick={() => wslink.spin(context.current, "PREV")}>Prev</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.spin(context.current, "NEXT")}>Next</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.activeWL(context.current)}>WL</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.applyWLPreset(context.current, 90, 35)}>Brain (90,25)</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.applyWLPreset(context.current, 4000, 700)}>Spine (4000,700)</Button> */}
        </Toolbar>
        <LinearProgress sx={{ opacity: !!busy ? 1 : 0 }} />
      </AppBar>

      <Box className="appContent">
        <div className="views">
          <div className="volume">
            <div style={{ position: "relative", width: "100%", height: "90%"}}>
              <RemoteRenderView client={client} viewId="1" />
            </div>
          </div>
          <div className="mpr">
            <div style={{ position: "relative", width: "100%", height: "30%", borderLeft: "0.5px groove white", borderBottom: "0.5px groove white" }}>
              <RemoteRenderView client={client} viewId="2" />
            </div>
            <div style={{ position: "relative", width: "100%", height: "30%", borderLeft: "0.5px groove white", borderBottom: "0.5px groove white" }}>
              <RemoteRenderView client={client} viewId="3" />
            </div>
            <div style={{ position: "relative", width: "100%", height: "30%", borderLeft: "0.5px groove white", borderBottom: "0.5px groove white" }}>
              <RemoteRenderView client={client} viewId="4" />
            </div>
          </div>
          {/* <div style={{ position: "relative", width: "300px", height: "200px", border: "0.5px groove white" }}>
            <RemoteRenderView client={client} viewId="1" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "200px", border: "0.5px groove white" }}>
            <RemoteRenderView client={client} viewId="2" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "200px", border: "0.5px groove white" }}>
            <RemoteRenderView client={client} viewId="3" />
          </div>
          <div style={{ position: "relative", width: "300px", height: "200px", border: "0.5px groove white" }}>
            <RemoteRenderView client={client} viewId="4" />
          </div> */}
        </div>
      </Box>
    </Box>
  );
}

export default App;
