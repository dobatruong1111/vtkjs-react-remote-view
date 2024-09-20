/* eslint-disable arrow-body-style */
export default function createMethods(session) {
  return {
    createVisualization: () => session.call('volume.initialize', []),
    shading: () => session.call('volume.shade', []),
    createNewVisualization: (seriesUID) => session.call('volume.create', [seriesUID]),
    activeRotate: () => session.call('volume.rotate', []),
    rotateDirection: (direction) => session.call('volume.view.plane', [direction]),
    applyPreset: (name) => session.call('volume.preset', [name]),
    activeLength: () => session.call('volume.length', []),
    activeAngle: () => session.call('volume.angle', []),
    delete: () => session.call('volume.delete', []),
    activeCut: () => session.call('volume.crop', []),
    activeCutFreehand: () => session.call('volume.crop.freehand', ["INSIDE"]),
    removeBed: () => session.call('volume.remove.bed'),
    activePan: () => session.call('volume.pan', []),
    resetViewport: () => session.call('volume.reset', []),
    updateResolution: (resolution) =>
      session.call('vtk.cone.resolution.update', [resolution]),
    shift: () => session.call('volume.shift', [])
  };
}
