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
  // const [sessionURL, setSessionURL] = useState();

  console.log("re-render");

  // const fetchData = useCallback(() => {
  //   return axios.post("http://localhost:9000/websocketlink",
  //     {
  //       application: "viewer",
  //       studyUID: "1",
  //       seriesUID: "1.2",
  //       sessionId: "123"
  //     }
  //   );
  // }, []);

  useEffect(() => {
    console.log("before fetch data");

    // axios.post("http://localhost:9000/websocketlink",
    //   {
    //     application: "viewer",
    //     studyUID: "1",
    //     seriesUID: "1.2",
    //     sessionId: "123"
    //   }
    // ).then(function (response) {
    //   let wsURL = response.data?.body?.sessionUrl;
    //   if (wsURL) {
    //     console.log("after fetch data");
    //     setSessionURL(wsURL);
    //     wslink.connect(context.current, setClient, setBusy, wsURL);
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

  // const resetCamera = () => {
  //   wslink.resetCamera(context.current);
  // }

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* <AppBar position="static" color="inherit">
        <Toolbar>
          <img src={logo} alt="logo" className="logo"></img>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Application
          </Typography>

          <Slider
            value={resolution}
            onChange={updateResolution}
            min={4}
            max={60}
            step={1}
            sx={{ maxWidth: "300px" }}
          />
          <IconButton onClick={resetCamera}>
            <CameraAlt />
          </IconButton>
        </Toolbar>
        <LinearProgress sx={{ opacity: !!busy ? 1 : 0 }} />
      </AppBar> */}

      <Box className="appContent">
        <div style={{ position: "relative", width: "100%", height: "100%" }}>
          <RemoteRenderView client={client} />
        </div>
      </Box>
    </Box>
  );
}

export default App;
