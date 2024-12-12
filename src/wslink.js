import vtkWSLinkClient from "vtk.js/Sources/IO/Core/WSLinkClient";
import SmartConnect from "wslink/src/SmartConnect";

import protocols from "./protocols";

import { connectImageStream } from "vtk.js/Sources/Rendering/Misc/RemoteView";

vtkWSLinkClient.setSmartConnectClass(SmartConnect);

const TOPIC = "wslink.channel";

const wslink = {
  connect: (context, setClient, setBusy, sessionURL) => {

    // Initiate network connection
    const config = {
      application: "cone",
      sessionURL: sessionURL
    };

    // We suppose that we have dev server and that ParaView/VTK is running on port 1234
    // config.sessionURL = `ws://${window.location.hostname}:1234/ws`;
    // config.sessionURL = sessionURL;

    const client = context.client;
    if (client && client.isConnected()) {
      client.disconnect(-1);
    }
    let clientToConnect = client;
    if (!clientToConnect) {
      clientToConnect = vtkWSLinkClient.newInstance({ protocols });
    }

    // Connect to busy store
    clientToConnect.onBusyChange((busy) => {
      setBusy(busy);
    });
    clientToConnect.beginBusy();

    // Error
    clientToConnect.onConnectionError((httpReq) => {
      const message =
        (httpReq && httpReq.response && httpReq.response.error) ||
        `Connection error`;
      console.error(message);
      console.log(httpReq);
    });

    // Close
    clientToConnect.onConnectionClose((httpReq) => {
      const message =
        (httpReq && httpReq.response && httpReq.response.error) ||
        `Connection close`;
      console.error(message);
      console.log(httpReq);
    });

    // Connect
    clientToConnect
      .connect(config)
      .then((validClient) => {
        connectImageStream(validClient.getConnection().getSession());
        context.client = validClient;
        setClient(context.client);
        clientToConnect.endBusy();

        // Now that the client is ready let's setup the server for us
        if (context.client) {
          // console.log(context.client);
          context.client.getRemote().Cone.createVisualization().catch(console.error);
        }
      })
      .catch((error) => {
        console.error(error);
      });
  },
  createVolume: (context) => {
    if (context.client) {
      context.client
        .getRemote()
        .Cone.createVisualization()
        .catch(console.error);
    }
  },
  delete: (context) => {
    if (context.client) {
      context.client
        .getRemote()
        .Cone.delete()
        .catch(console.error);
    }
  },
  shading: (context) => {
    if (context.client) {
      context.client
        .getRemote()
        .Cone.shading()
        .catch(console.error);
    }
  },
  initializeServer: (context) => {
    if (context.client) {
      context.client
        .getRemote()
        .Cone.createVisualization()
        .catch(console.error);
    }
  },
  reinitializeServer: (context) => {
    if (context.client) {
      context.client
        .getRemote()
        .Cone.createNewVisualization()
        .catch(console.error);
    }
  },
  updateResolution: (context, resolution) => {
    if (context.client) {
      // console.log(resolution);
      context.client
        .getRemote()
        .Cone.updateResolution(resolution)
        .catch(console.error);
    }
  },
  resetViewport: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.resetViewport().catch(console.error);
    }
  },
  applyPreset: (context, name) => {
    if (context.client) {
      context.client.getRemote().Cone.applyPreset(name).catch(console.error);
    }
  },
  shift: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.shift().catch(console.error);
    }
  },
  activeLength: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeLength().catch(console.error);
    }
  },
  activeAngle: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeAngle().catch(console.error);
    }
  },
  activeCut: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeCut().catch(console.error);
    }
  },
  activeCutFreehand: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeCutFreehand().catch(console.error);
    }
  },
  removeBed: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.removeBed().catch(console.error);
    }
  },
  activePan: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activePan().catch(console.error);
    }
  },
  activeZoom: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeZoom().catch(console.error);
    }
  },
  activeRotate: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeRotate().catch(console.error);
    }
  },
  rotateDirection: (context, direction) => {
    if (context.client) {
      context.client.getRemote().Cone.rotateDirection(direction).catch(console.error);
    }
  },
  dicomDownload: (context, studyUID, seriesUID) => {
    if (context.client) {
      context.client.getRemote().Cone.dicomDownload(studyUID, seriesUID).catch(console.error);
    }
  },
  getStatus: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.getStatus().catch(console.error);
    }
  },
  turnOnSlice3D: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.turnOnSlice3D().catch(console.error);
    }
  },
  turnOffSlice3D: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.turnOffSlice3D().catch(console.error);
    }
  },
  slice3D: (context, orientation) => {
    if (context.client) {
      context.client.getRemote().Cone.slice3D(orientation).catch(console.error);
    }
  },
  flythrough: (context, operation) => {
    if(context.client) {
      context.client.getRemote().Cone.flythrough(operation).catch(console.error);
    }
  },
  resetEndo: (context) => {
    if(context.client) {
      context.client.getRemote().Cone.resetEndo().catch(console.error);
    }
  },
  setCrosslines: (context) => {
    if(context.client) {
      context.client.getRemote().Cone.setCrosslines().catch(console.error);
    }
  },
  spin: (context, option) => {
    if(context.client) {
      context.client.getRemote().Cone.spin(option).catch(console.error);
    }
  },
  activeWL: (context) => {
    if (context.client) {
      context.client.getRemote().Cone.activeWL().catch(console.error);
    }
  },
  applyWLPreset: (context, ww, wl) => {
    if (context.client) {
      context.client.getRemote().Cone.applyWLPreset(ww, wl).catch(console.error);
    }
  }
};

export default wslink;
