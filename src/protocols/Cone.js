/* eslint-disable arrow-body-style */
export default function createMethods(session) {
  return {
    createVisualization: () => session.call('volume.initialize', []),
    applyBonePresetCT: () => session.call('volume.bone.preset.ct', []),
    applyAngioPresetCT: () => session.call('volume.angio.preset.ct', []),
    applyMusclePresetCT: () => session.call('volume.muscle.preset.ct', []),
    applyMipPresetCT: () => session.call('volume.mip.preset.ct', []),
    activeLength: () => session.call('volume.length', []),
    activeAngle: () => session.call('volume.angle', []),
    activeCut: () => session.call('volume.cut', []),
    activeCutFreehand: () => session.call('volume.cut.freehand', []),
    activePan: () => session.call('volume.pan', []),
    resetCamera: () => session.call('volume.reset', []),
    updateResolution: (resolution) =>
      session.call('vtk.cone.resolution.update', [resolution]),
  };
}
