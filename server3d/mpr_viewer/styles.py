import vtk

class BaseImageInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, viewer) -> None:
        self.viewer = viewer

        self.left_pressed = False
        self.middle_pressed = False
        self.right_pressed = False

        self.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.OnPressLeftButton)
        self.AddObserver(vtk.vtkCommand.LeftButtonReleaseEvent, self.OnReleaseLeftButton)
        self.AddObserver(vtk.vtkCommand.MiddleButtonPressEvent, self.OnMiddleButtonPressEvent)
        self.AddObserver(vtk.vtkCommand.MiddleButtonReleaseEvent, self.OnMiddleButtonReleaseEvent)
        self.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.OnPressRightButton)
        self.AddObserver(vtk.vtkCommand.RightButtonReleaseEvent, self.OnReleaseRightButton)

    def OnPressLeftButton(self, obj, event) -> None:
        self.left_pressed = True

    def OnReleaseLeftButton(self, obj, event) -> None:
        self.left_pressed = False

    def OnMiddleButtonPressEvent(self, obj, event) -> None:
        self.middle_pressed = True

    def OnMiddleButtonReleaseEvent(self, obj, event) -> None:
        self.middle_pressed = False

    def OnPressRightButton(self, obj, event) -> None:
        self.right_pressed = True

    def OnReleaseRightButton(self, obj, event) -> None:
        self.right_pressed = False

class DefaultInteractorStyle(BaseImageInteractorStyle):
    def __init__(self, viewer, orientation) -> None:
        BaseImageInteractorStyle.__init__(self, viewer)

        self.viewer = viewer
        self.orientation = orientation

        self.AddObserver(vtk.vtkCommand.MouseMoveEvent, self.OnZoomRightMove)
        self.AddObserver(vtk.vtkCommand.MouseWheelForwardEvent, self.OnScrollForward)
        self.AddObserver(vtk.vtkCommand.MouseWheelBackwardEvent, self.OnScrollBackward)
        # Zoom using right button
        self.AddObserver(vtk.vtkCommand.RightButtonPressEvent, self.OnZoomRightClick)
        self.AddObserver(vtk.vtkCommand.RightButtonReleaseEvent, self.OnZoomRightRelease)

    def OnZoomRightMove(self, obj, event) -> None:
        if self.right_pressed:
            # obj.Dolly()
            obj.Rotate()
            obj.OnRightButtonDown()
        elif self.middle_pressed:
            obj.Pan()
            obj.OnMiddleButtonDown()

    def OnScrollForward(self, obj, event) -> None:
        self.viewer.OnScrollForward(self.orientation)

    def OnScrollBackward(self, obj, event) -> None:
        self.viewer.OnScrollBackward(self.orientation)

    def OnZoomRightClick(self, obj, event) -> None:
        # obj.StartDolly()
        obj.StartRotate()

    def OnZoomRightRelease(self, obj, event) -> None:
        obj.OnRightButtonUp()
        self.right_pressed = False

class CrossInteractorStyle(DefaultInteractorStyle):
    def __init__(self, viewer, orientation) -> None:
        DefaultInteractorStyle.__init__(self, viewer, orientation)

        self.viewer = viewer
        self.orientation = orientation
        self.picker = vtk.vtkWorldPointPicker()

        self.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.OnCrossMouseClick)
        self.AddObserver(vtk.vtkCommand.MouseMoveEvent, self.OnCrossMove)

    def OnCrossMouseClick(self, obj, event) -> None:
        iren = obj.GetInteractor()
        self.ChangeCrossPosition(iren)

    def OnCrossMove(self, obj, event) -> None:
        # The user moved the mouse with left button pressed.
        if self.left_pressed:
            iren = obj.GetInteractor()
            self.ChangeCrossPosition(iren)

    def ChangeCrossPosition(self, iren: vtk.vtkRenderWindowInteractor) -> None:
        mouse_x, mouse_y = iren.GetEventPosition()
        x, y, z = self.viewer.get_coordinate_cursor(mouse_x, mouse_y, self.orientation, self.picker)
        self.viewer.UpdateSlicesPosition(self.orientation, [x, y, z])
        # Update the position of the cross in other slices.
        self.viewer.SetCrossFocalPoint([x, y, z])
        self.viewer.UpdateRender()

    def OnScrollBar(self) -> None:
        if self.orientation == "AXIAL":
            x, y, z = self.viewer.cross_axial.GetFocalPoint()
        elif self.orientation == "CORONAL":
            x, y, z = self.viewer.cross_coronal.GetFocalPoint()
        elif self.orientation == "SAGITAL":
            x, y, z = self.viewer.cross_sagital.GetFocalPoint()

        self.viewer.UpdateSlicesPosition(self.orientation, [x, y, z])
        # Update the position of the cross in other slices.
        self.viewer.SetCrossFocalPoint([x, y, z])
        self.viewer.UpdateRender()

class CrossInteractorStyle_2(DefaultInteractorStyle):
    def __init__(self, viewer, orientation) -> None:
        DefaultInteractorStyle.__init__(self, viewer, orientation)

        self.viewer = viewer
        self.orientation = orientation
        self.picker = vtk.vtkWorldPointPicker()

        self.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.OnCrossMouseClick)
        self.AddObserver(vtk.vtkCommand.LeftButtonReleaseEvent, self.OnReleaseLeftButton)
        self.AddObserver(vtk.vtkCommand.MouseMoveEvent, self.OnCrossMove)

    def OnCrossMouseClick(self, obj, event) -> None:
        iren = obj.GetInteractor()
        mouse_x, mouse_y = iren.GetEventPosition()
        x, y, z = self.viewer.get_coordinate_cursor(mouse_x, mouse_y, self.orientation, self.picker)
        self.viewer.SetCrossFocalPoint([x, y, z])
        self.viewer.UpdateRender()

    def OnReleaseLeftButton(self, obj, event) -> None:
        iren = obj.GetInteractor()
        mouse_x, mouse_y = iren.GetEventPosition()
        x, y, z = self.viewer.get_coordinate_cursor(mouse_x, mouse_y, self.orientation, self.picker)
        self.viewer.UpdateSlicesPosition(self.orientation, [x, y, z])
        self.viewer.UpdateRender()
        # self.viewer.UpdateCameraPosition([x, y, z])
        # self.viewer.UpdateRenderVolume()

    def OnCrossMove(self, obj, event) -> None:
        if self.left_pressed:
            iren = obj.GetInteractor()
            mouse_x, mouse_y = iren.GetEventPosition()
            x, y, z = self.viewer.get_coordinate_cursor(mouse_x, mouse_y, self.orientation, self.picker)
            self.viewer.SetCrossFocalPoint([x, y, z])
            self.viewer.UpdateRender()
