import React, { useEffect, useRef } from 'react';
// import vtkRemoteView from 'vtk.js/Sources/Rendering/Misc/RemoteView';
import './RemoteRenderingView.css'
import vtkRemoteView from "vtk.js/Sources/Rendering/Misc/RemoteView";


const RemoteRenderView = ({ viewId = '-1', client = null }) => {
  const viewRef = useRef(null);
  const view = useRef(null);
  
  useEffect(() => {
    view.current = vtkRemoteView.newInstance({
      rpcWheelEvent: "viewport.mouse.zoom.wheel",
    });
    // default of 0.5 causes 2x size labels on high-DPI screens. 1 good for demo, not for production.
    if (window.location.hostname.split(".")[0] === "localhost") {
      view.current.setInteractiveRatio(1);
    }

    view.current.setContainer(viewRef.current);
    window.addEventListener("resize", view.current.resize);

    if (client) {
      // console.log('RemoteRenderView', this.viewId);
      const session = client.getConnection().getSession();
      view.current.setSession(session);
      view.current.setViewId(viewId);
      view.current.render();
    }
  }, [client, viewId]);

  return (
    <div ref={viewRef} className="container"></div>
  );
};

export default RemoteRenderView;
