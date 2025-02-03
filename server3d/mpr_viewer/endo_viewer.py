import vtk

from slice_ import Slice
from converters import to_vtk

class EndoscopyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self) -> None:
        super().__init__()
        self.AddObserver(vtk.vtkCommand.MouseWheelForwardEvent, self.OnScrollForward)
        self.AddObserver(vtk.vtkCommand.MouseWheelBackwardEvent, self.OnScrollBackward)
        self.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.OnZoomRightPress)
        self.AddObserver(vtk.vtkCommand.RightButtonReleaseEvent, self.OnZoomRightRelease)

    def OnScrollForward(self, obj, event) -> None:
        pass

    def OnScrollBackward(self, obj, event) -> None:
        pass

    def OnZoomRightPress(self, obj, event) -> None:
        pass

    def OnZoomRightRelease(self, obj, event) -> None:
        pass

class EndoscopyViewer:
    def __init__(self) -> None:
        pass

    def LoadImage(self) -> None:
        slice_data = Slice()
        n_array = slice_data.matrix
        spacing = slice_data.spacing
        image = to_vtk(n_array, spacing)
        self.image = image
    
    def LoadVolume(self) -> None:
        self.LoadImage()
        image = self.image

        # GPU
        volume_mapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
        volume_mapper.SetInputData(image)
        volume_mapper.AutoAdjustSampleDistancesOff()
        volume_mapper.LockSampleDistanceToInputSpacingOn()
        # CPU
        # volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
        # volume_mapper.SetAutoAdjustSampleDistances(True)
        # volume_mapper.SetLockSampleDistanceToInputSpacing(False)
        # volume_mapper.SetImageSampleDistance(1.0)
        # volume_mapper.SetInputData(image)
        # spacing = image.GetSpacing()
        # sampleDistance = (spacing[0] + spacing[1] + spacing[2])/6
        # volume_mapper.SetSampleDistance(sampleDistance)
        # volume_mapper.SetInteractiveSampleDistance(sampleDistance)

        volume_properties = vtk.vtkVolumeProperty()
        volume_properties.SetInterpolationTypeToLinear()
        volume_properties.ShadeOn()

        volume_properties.SetAmbient(0.15)
        volume_properties.SetDiffuse(0.9)
        volume_properties.SetSpecular(0.3)
        volume_properties.SetSpecularPower(15)

        scalar_color = vtk.vtkColorTransferFunction()
        scalar_color.AddRGBPoint(-1000, 0, 0, 0)
        scalar_color.AddRGBPoint(-600, 194 / 255, 105 / 255, 82 / 255)
        scalar_color.AddRGBPoint(-400, 194 / 255, 105 / 255, 82 / 255)
        scalar_color.AddRGBPoint(-100, 194 / 255, 166 / 255, 115 / 255)
        scalar_color.AddRGBPoint(-60, 194 / 255, 166 / 255, 115 / 255)
        scalar_color.AddRGBPoint(40, 102 / 255, 0, 0)
        scalar_color.AddRGBPoint(80, 153 / 255, 0, 0)
        scalar_color.AddRGBPoint(400, 255 / 255, 217 / 255, 163 / 255)
        scalar_color.AddRGBPoint(1000, 255 / 255, 217 / 255, 163 / 255)
        volume_properties.SetColor(scalar_color)

        scalar_opacity = vtk.vtkPiecewiseFunction()
        scalar_opacity.AddPoint(-1000, 0)
        scalar_opacity.AddPoint(-400, 0)
        scalar_opacity.AddPoint(400, 1)
        scalar_opacity.AddPoint(1000, 1)
        volume_properties.SetScalarOpacity(scalar_opacity)

        gradient_opacity = vtk.vtkPiecewiseFunction()
        gradient_opacity.AddPoint(0, 1)
        gradient_opacity.AddPoint(255, 1)
        volume_properties.SetGradientOpacity(gradient_opacity)
        self.volume_properties = volume_properties

        volume = vtk.vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_properties)
        self.volume = volume
