/* eslint-disable arrow-body-style */
export default function createMethods(session) {
  return {
    createVisualization: () => session.call('volume.initialize', []),
    shading: () => session.call('volume.shade', []),
    createNewVisualization: () => session.call('volume.create', ["1.2.840.113619.2.415.3.2831155460.530.1721039812.503.3"]),
    activeRotate: () => session.call('volume.rotate', []),
    rotateDirection: (direction) => session.call('volume.view.plane', [direction]),
    applyPreset: (name) => session.call('volume.preset', [name]),
    activeLength: () => session.call('volume.length', []),
    activeAngle: () => session.call('volume.angle', []),
    delete: () => session.call('volume.delete', []),
    activeCut: () => session.call('volume.crop', []),
    activeCutFreehand: () => session.call('volume.crop.freehand', ["INSIDE"]),
    activePan: () => session.call('volume.pan', []),
    resetViewport: () => session.call('volume.reset', []),
    updateResolution: (resolution) =>
      session.call('vtk.cone.resolution.update', [resolution]),
  };
}
