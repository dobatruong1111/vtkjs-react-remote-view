import { useState, useRef, useEffect } from "react";
import wslink from "./wslink";
import "./App.css";
import {
  Box,
  AppBar,
  Toolbar,
  LinearProgress,
  Button,
} from "@mui/material";
import RemoteRenderView from "./RemoteRenderingView";
// import ClientRenderingView from "./ClientRenderingView";
// import RemoteRenderView2 from "./RemoteRenderingView2";
// import axios from "axios";

const TOPIC = "mpr.channel";
function App() {
  const context = useRef({});
  const [client, setClient] = useState(null);
  const [busy, setBusy] = useState(0);
  const [crosslinePositions, setCrosslinePositions] = useState(null);

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

    // axios.post("http://192.168.1.6:8888/ws/rest/v1/session3d/websocketlink",
    //   {
    //     session2D: "47ffdf80-43a6-4ca9-95ef-e83e9c00a5b8",
    //     studyUID: "2.25.273770070420816203849299146355226291780",
    //     seriesUID: "1.2.840.113619.2.428.3.678656.566.1723853370.188.3"
    //   }
    // ).then(function (response) {
    //   let wsURL = response.data?.websocketUrl;
    //   if (wsURL) {
    //     let temp = `ws://192.168.1.6:8888${wsURL}`;
    //     wslink.connect(context.current, setClient, setBusy, temp);
    //   }
    // }).catch(function (error) {
    //   console.log("error: ", error);
    // })

    const wsURL = "ws://localhost:1234/ws";
    wslink.connect(context.current, setClient, setBusy, wsURL);
  }, []);

  useEffect(() => {
    if (client) {
      const session = client.getConnection().getSession();
      session.subscribe(TOPIC, ([msg]) => {
        setCrosslinePositions(msg);
      });
    }
  }, [client]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="inherit">
        <Toolbar>
          <Button variant="outlined" onClick={() => wslink.reinitializeServer(context.current)}>Download</Button>
          <Button variant="outlined" onClick={() => wslink.createVolume(context.current)}>Create</Button>
          <Button variant="outlined" onClick={() => wslink.shift(context.current)}>WL</Button>
          <Button variant="outlined" onClick={() => wslink.activeRotate(context.current)}>Rotate</Button>
          <Button variant="outlined" onClick={() => wslink.activeZoom(context.current)}>Zoom</Button>
          <Button variant="outlined" onClick={() => wslink.activePan(context.current)}>Pan</Button>
          {/* <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "CT-AAA")}>CT-AAA</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "CT-AAA-Bone")}>CT-AAA-Bone</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "MR-Default-TOF-GE")}>MR-GE</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "MR-Default-TOF-Hitachi")}>MR-Hitachi</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "MR-Default-TOF-Philips")}>MR-Philips</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "MR-Default-TOF-Siemens")}>MR-Siemens</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "MR-Default-TOF-UIH")}>MR-UIH</Button>
          <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "Standard")}>Standard</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.applyPreset(context.current, "Soft + Skin")}>Soft + Skin</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.activeLength(context.current)}>Length</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.activeAngle(context.current)}>Angle</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.delete(context.current)}>Delete</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.activeCut(context.current)}>Crop</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.activeCutFreehand(context.current)}>Freehand</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.removeBed(context.current)}>Bed</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.shading(context.current)}>Shade</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.dicomDownload(context.current, "1.2.840.113619.2.438.3.2831208971.408.1719531439.122", "1.2.840.113619.2.438.3.2831208971.408.1719531439.198")}>download</Button> */}
          <Button variant="outlined" onClick={() => wslink.slice3D(context.current, ["AXIAL", "CORONAL", "SAGITAL"])}>Turn on</Button>
          <Button variant="outlined" onClick={() => wslink.slice3D(context.current, [])}>Turn off</Button>
          {/* <Button variant="outlined" onClick={() => wslink.setCrosslines(context.current, [])}>Crosslines</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.test(context.current)}>Test</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.flythrough(context.current, "PREV")}>Endo-Prev</Button>
          <Button variant="outlined" onClick={() => wslink.flythrough(context.current, "NEXT")}>Endo-Next</Button>
          <Button variant="outlined" onClick={() => wslink.flythrough(context.current, "REVERT")}>Endo-Revert</Button> */}
          <Button variant="outlined" onClick={() => wslink.resetViewport(context.current)}>Reset</Button>
          {/* <Button variant="outlined" onClick={() => wslink.spin(context.current, "PREV")}>Prev</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.spin(context.current, "NEXT")}>Next</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.activeWL(context.current)}>WL</Button> */}
          {/* <Button variant="outlined" onClick={() => wslink.test(context.current)}>Message</Button> */}
        </Toolbar>
        <LinearProgress sx={{ opacity: !!busy ? 1 : 0 }} />
      </AppBar>
      <Box className="appContent">
        <div className="views">
          {/* <div className="volume">
            <div id="volume" style={{ position: "relative", width: "100%", height: "90%"}}>
              <RemoteRenderView
                client={client}
                viewId="1"
                crosslineColor={["red", "blue"]}
                crosslinePositions={crosslinePositions}
              />
            </div>
          </div>
          <div className="mpr">
            <div id="axial" style={{ position: "relative", width: "100%", height: "30%", borderLeft: "0.5px groove white", borderBottom: "0.5px groove white" }}>
              <RemoteRenderView
                client={client}
                viewId="2"
                crosslineColor={["red", "blue"]}
                crosslinePositions={crosslinePositions}
              />
            </div>
            <div id="coronal" style={{ position: "relative", width: "100%", height: "30%", borderLeft: "0.5px groove white", borderBottom: "0.5px groove white" }}>
              <RemoteRenderView
                client={client}
                viewId="3"
                crosslineColor={["red", "green"]}
                crosslinePositions={crosslinePositions}
              />
            </div>
            <div id="sagital" style={{ position: "relative", width: "100%", height: "30%", borderLeft: "0.5px groove white", borderBottom: "0.5px groove white" }}>
              <RemoteRenderView
                client={client}
                viewId="4"
                crosslineColor={["blue", "green"]}
                crosslinePositions={crosslinePositions}
              />
            </div>
          </div> */}
          <div style={{ position: "relative", width: "600px", height: "600px", border: "0.5px groove white" }}>
            <RemoteRenderView
              client={client}
              viewId="1"
              crosslineColor={null}
              crosslinePositions={null}
            />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px", border: "0.5px groove white" }}>
            <RemoteRenderView
              client={client}
              viewId="2"
              crosslineColor={["green", "blue"]}
              crosslinePositions={crosslinePositions}
            />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px", border: "0.5px groove white" }}>
            <RemoteRenderView
              client={client}
              viewId="3"
              crosslineColor={["green", "red"]}
              crosslinePositions={crosslinePositions}
            />
          </div>
          <div style={{ position: "relative", width: "300px", height: "300px", border: "0.5px groove white" }}>
            <RemoteRenderView
              client={client}
              viewId="4"
              crosslineColor={["blue", "red"]}
              crosslinePositions={crosslinePositions}
            />
          </div>
        </div>
      </Box>
    </Box>
    // <ClientRenderingView />
  );
}

export default App;
