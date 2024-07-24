/* eslint-disable arrow-body-style */
export default function createMethods(session) {
  return {
    createVisualization: () => session.call('volume.initialize', []),
    activeRotate: () => session.call('volume.rotate', []),
    applyPreset: () => session.call('volume.preset', ["CT-Cardiac"]),
    activeLength: () => session.call('volume.length', []),
    activeAngle: () => session.call('volume.angle', []),
    activeCut: () => session.call('volume.cut', []),
    activeCutFreehand: () => session.call('volume.cut.freehand', []),
    activePan: () => session.call('volume.pan', []),
    resetViewport: () => session.call('volume.reset', []),
    updateResolution: (resolution) =>
      session.call('vtk.cone.resolution.update', [resolution]),
  };
}
