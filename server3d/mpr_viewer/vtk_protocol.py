from vtk.web import protocols as vtk_protocols # type: ignore
from wslink import register as exportRpc
import vtk
from vtkmodules.util.numpy_support import vtk_to_numpy
from typing import List, Tuple

from slice_data import SliceData
from slice_ import Slice
from styles import CrossInteractorStyle, CrossInteractorStyle_2
from project import Project
from vtk_utils import TextZero
import constants as const
from volume_viewer import VolumeViewer
from endo_viewer import EndoscopyViewer

class VtkCone(vtk_protocols.vtkWebProtocol):
    def __init__(self) -> None:
        self.number_slices = 1
        self.scroll_position_axial = 0
        self.scroll_position_coronal = 0
        self.scroll_position_sagital = 0
        self.picker = vtk.vtkWorldPointPicker()
        self.last_position = None

    def create_slice_window(self, orientation: str) -> SliceData:
        renderer = vtk.vtkRenderer()
        renderer.SetLayer(0)
        cam = renderer.GetActiveCamera()

        overlay_renderer = vtk.vtkRenderer()
        overlay_renderer.SetLayer(1)
        overlay_renderer.SetActiveCamera(cam)
        overlay_renderer.SetInteractive(0)

        if orientation == "AXIAL":
            render_window = self.getApplication().GetObjectIdMap().GetActiveObject("AXIAL_VIEW")
        elif orientation == "CORONAL":
            render_window = self.getApplication().GetObjectIdMap().GetActiveObject("CORONAL_VIEW")
        else:
            render_window = self.getApplication().GetObjectIdMap().GetActiveObject("SAGITAL_VIEW")

        render_window.SetNumberOfLayers(2)
        render_window.AddRenderer(overlay_renderer)
        render_window.AddRenderer(renderer)
        
        actor = vtk.vtkImageActor()
        actor.InterpolateOn()

        slice_data = SliceData()
        slice_data.SetOrientation(orientation)
        slice_data.actor = actor
        slice_data.renderer = renderer
        slice_data.overlay_renderer = overlay_renderer

        renderer.AddActor(actor)
        # renderer.AddActor(slice_data.text.actor)
        
        return slice_data
    
    def update_display_extent(self, image: vtk.vtkImageData, orientation: str) -> None:
        if orientation == "AXIAL":
            self.slice_data_axial.actor.SetDisplayExtent(image.GetExtent())
            self.slice_data_axial.renderer.ResetCameraClippingRange()
        elif orientation == "CORONAL":
            self.slice_data_coronal.actor.SetDisplayExtent(image.GetExtent())
            self.slice_data_coronal.renderer.ResetCameraClippingRange()
        else:
            self.slice_data_sagital.actor.SetDisplayExtent(image.GetExtent())
            self.slice_data_sagital.renderer.ResetCameraClippingRange()
    
    def set_slice_number(self, index: int, orientation: str) -> None:
        index = max(index, 0)
        index = min(index, self.slice.GetNumberOfSlices(orientation) - 1)
        image = self.slice.GetSlices(orientation, index, self.number_slices)
        if orientation == "AXIAL":
            self.slice_data_axial.actor.SetInputData(image)
            self.slice_data_axial.SetNumber(index)

            self.update_display_extent(image, orientation)

            bounds = self.slice_data_axial.actor.GetBounds()
            # self.cross_axial.SetModelBounds(self.slice_data_axial.actor.GetBounds())
            self.cross_axial.SetModelBounds(bounds[0] - 2*bounds[1], bounds[1] + 2*bounds[1], bounds[2] - 2*bounds[3], bounds[3] + 2*bounds[3], bounds[4], bounds[5])
            self.cross_axial.Update()
            self.cross_axial.GetOutput().GetCellData().SetScalars(self.color_array_axial)
        elif orientation == "CORONAL":
            self.slice_data_coronal.actor.SetInputData(image)
            self.slice_data_coronal.SetNumber(index)

            self.update_display_extent(image, orientation)

            bounds = self.slice_data_coronal.actor.GetBounds()
            # self.cross_coronal.SetModelBounds(self.slice_data_coronal.actor.GetBounds())
            self.cross_coronal.SetModelBounds(bounds[0] - 3*bounds[1], bounds[1] + 3*bounds[1], bounds[2], bounds[3], bounds[4] - 3*bounds[5], bounds[5] + 3*bounds[5])
            self.cross_coronal.Update()
            self.cross_coronal.GetOutput().GetCellData().SetScalars(self.color_array_coronal)
        else:
            self.slice_data_sagital.actor.SetInputData(image)
            self.slice_data_sagital.SetNumber(index)

            self.update_display_extent(image, orientation)

            bounds = self.slice_data_sagital.actor.GetBounds()
            # self.cross_sagital.SetModelBounds(self.slice_data_sagital.actor.GetBounds())
            self.cross_sagital.SetModelBounds(bounds[0], bounds[1], bounds[2] - 3*bounds[3], bounds[3] + 3*bounds[3], bounds[4] - 3*bounds[5], bounds[5] + 3*bounds[5])
            self.cross_sagital.Update()
            self.cross_sagital.GetOutput().GetCellData().SetScalars(self.color_array_sagital)

    def update_camera(self, orientation: str) -> None:
        if orientation == "AXIAL":
            renderer = self.slice_data_axial.renderer
            camera = renderer.GetActiveCamera()
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 1, 0)
            camera.SetPosition(0, 0, 1)
        elif orientation == "CORONAL":
            renderer = self.slice_data_coronal.renderer
            camera = renderer.GetActiveCamera()
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 0, -1)
            camera.SetPosition(0, 1, 0)
        else:
            renderer = self.slice_data_sagital.renderer
            camera = renderer.GetActiveCamera()
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 0, -1)
            camera.SetPosition(-1, 0, 0)
        camera.ParallelProjectionOn()
        renderer.ResetCamera()
        # Zoom camera
        if orientation == "AXIAL":
            camera.Zoom(1.2)
        elif orientation == "CORONAL":
            camera.Zoom(1.2)
        else:
            camera.Zoom(1.2)

    def SetInteractorStyle(self) -> None:
        render_window_axial = self.getApplication().GetObjectIdMap().GetActiveObject("AXIAL_VIEW")
        interactor_axial = render_window_axial.GetInteractor()
        # style_axial = CrossInteractorStyle_2(self, "AXIAL")
        style_axial = vtk.vtkInteractorStyle()
        interactor_axial.SetInteractorStyle(style_axial)

        render_window_coronal = self.getApplication().GetObjectIdMap().GetActiveObject("CORONAL_VIEW")
        interactor_coronal = render_window_coronal.GetInteractor()
        # style_coronal = CrossInteractorStyle_2(self, "CORONAL")
        style_coronal = vtk.vtkInteractorStyle()
        interactor_coronal.SetInteractorStyle(style_coronal)

        render_window_sagital = self.getApplication().GetObjectIdMap().GetActiveObject("SAGITAL_VIEW")
        interactor_sagital = render_window_sagital.GetInteractor()
        # style_sagital = CrossInteractorStyle_2(self, "SAGITAL")
        style_sagital = vtk.vtkInteractorStyle()
        interactor_sagital.SetInteractorStyle(style_sagital)

    def UpdateRender(self, orientation=None) -> None:
        render_window_axial = self.getApplication().GetObjectIdMap().GetActiveObject("AXIAL_VIEW")
        render_window_coronal = self.getApplication().GetObjectIdMap().GetActiveObject("CORONAL_VIEW")
        render_window_sagital = self.getApplication().GetObjectIdMap().GetActiveObject("SAGITAL_VIEW")
        if orientation is None:
            render_window_axial.Render()
            render_window_coronal.Render()
            render_window_sagital.Render()
        elif orientation == "AXIAL":
            render_window_coronal.Render()
            render_window_sagital.Render()
        elif orientation == "CORONAL":
            render_window_axial.Render()
            render_window_sagital.Render()
        elif orientation == "SAGITAL":
            render_window_axial.Render()
            render_window_coronal.Render()

    def UpdateRenderVolume(self) -> None:
        render_window_volume = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        render_window_volume.Render()

    def build_cross_lines(self) -> None:
        # Generate a 3D cursor representation.
        cross_axial = vtk.vtkCursor3D()
        # Turn every part of the 3D cursor on or off.
        cross_axial.AllOff()
        # Turn on/off the wireframe axes.
        cross_axial.AxesOn()
        self.cross_axial = cross_axial
        # Create a vtkUnsignedCharArray container and store the colors in it
        color_array_axial = vtk.vtkUnsignedCharArray()
        color_array_axial.SetNumberOfComponents(3)
        color_array_axial.SetNumberOfTuples(3)
        color_array_axial.SetTuple(0, [0, 0, 255])
        color_array_axial.SetTuple(1, [0, 255, 0])
        color_array_axial.SetTuple(2, [255, 0, 0])
        self.color_array_axial = color_array_axial
        # Create an actor
        cross_mapper_axial = vtk.vtkPolyDataMapper()
        cross_mapper_axial.SetInputConnection(cross_axial.GetOutputPort())
        cross_actor_axial = vtk.vtkActor()
        cross_actor_axial.SetMapper(cross_mapper_axial)
        # cross_actor_axial.GetProperty().SetColor(1, 0, 0)
        cross_actor_axial.GetProperty().SetLineWidth(2)
        cross_actor_axial.VisibilityOn()
        cross_actor_axial.PickableOff()
        self.cross_actor_axial = cross_actor_axial
        # Add actor
        self.slice_data_axial.overlay_renderer.AddActor(cross_actor_axial)

        # Generate a 3D cursor representation.
        cross_coronal = vtk.vtkCursor3D()
        # Turn every part of the 3D cursor on or off.
        cross_coronal.AllOff()
        # Turn on/off the wireframe axes.
        cross_coronal.AxesOn()
        self.cross_coronal = cross_coronal
        # Create a vtkUnsignedCharArray container and store the colors in it
        color_array_coronal = vtk.vtkUnsignedCharArray()
        color_array_coronal.SetNumberOfComponents(3)
        color_array_coronal.SetNumberOfTuples(3)
        color_array_coronal.SetTuple(0, [255, 0, 0])
        color_array_coronal.SetTuple(1, [0, 0, 255])
        color_array_coronal.SetTuple(2, [0, 255, 0])
        self.color_array_coronal = color_array_coronal
        # Create an actor
        cross_mapper_coronal = vtk.vtkPolyDataMapper()
        cross_mapper_coronal.SetInputConnection(cross_coronal.GetOutputPort())
        cross_actor_coronal = vtk.vtkActor()
        cross_actor_coronal.SetMapper(cross_mapper_coronal)
        # cross_actor_coronal.GetProperty().SetColor(1, 0, 0)
        cross_actor_coronal.GetProperty().SetLineWidth(2)
        cross_actor_coronal.VisibilityOn()
        cross_actor_coronal.PickableOff()
        self.cross_actor_coronal = cross_actor_coronal
        # Add actor
        self.slice_data_coronal.overlay_renderer.AddActor(cross_actor_coronal)

        # Generate a 3D cursor representation.
        cross_sagital = vtk.vtkCursor3D()
        # Turn every part of the 3D cursor on or off.
        cross_sagital.AllOff()
        # Turn on/off the wireframe axes.
        cross_sagital.AxesOn()
        self.cross_sagital = cross_sagital
        # Create a vtkUnsignedCharArray container and store the colors in it
        color_array_sagital = vtk.vtkUnsignedCharArray()
        color_array_sagital.SetNumberOfComponents(3)
        color_array_sagital.SetNumberOfTuples(3)
        color_array_sagital.SetTuple(0, [0, 255, 0])
        color_array_sagital.SetTuple(1, [255, 0, 0])
        color_array_sagital.SetTuple(2, [0, 0, 255])
        self.color_array_sagital = color_array_sagital
        # Create an actor
        cross_mapper_sagital = vtk.vtkPolyDataMapper()
        cross_mapper_sagital.SetInputConnection(cross_sagital.GetOutputPort())
        cross_actor_sagital = vtk.vtkActor()
        cross_actor_sagital.SetMapper(cross_mapper_sagital)
        # cross_actor_sagital.GetProperty().SetColor(1, 0, 0)
        cross_actor_sagital.GetProperty().SetLineWidth(2)
        cross_actor_sagital.VisibilityOn()
        cross_actor_sagital.PickableOff()
        # Add actor
        self.slice_data_sagital.overlay_renderer.AddActor(cross_actor_sagital)

    def EnableText(self, orientation: str) -> None:
        project = Project()

        # Window level text
        wl_text = TextZero()
        wl_text.SetSize(const.TEXT_SIZE_SMALL)
        wl_text.SetPosition(const.TEXT_POS_LEFT_UP)
        wl_text.SetValue("WL: %d WW: %d" % (project.window_level, project.window_width))

        # Orientation text
        if orientation == "AXIAL":
            values = ["R", "L", "A", "P"]
            renderer = self.slice_data_axial.overlay_renderer
        elif orientation == "SAGITAL":
            values = ["P", "A", "T", "B"]
            renderer = self.slice_data_sagital.overlay_renderer
        else:
            values = ["R", "L", "T", "B"]
            renderer = self.slice_data_coronal.overlay_renderer

        renderer.AddActor(wl_text.actor)

        left_text = TextZero()
        left_text.SetSize(const.TEXT_SIZE_SMALL)
        left_text.SetPosition(const.TEXT_POS_VCENTRE_LEFT)
        left_text.SetValue(values[0])
        renderer.AddActor(left_text.actor)

        right_text = TextZero()
        right_text.SetSize(const.TEXT_SIZE_SMALL)
        right_text.SetPosition(const.TEXT_POS_VCENTRE_RIGHT_ZERO)
        right_text.SetValue(values[1])
        renderer.AddActor(right_text.actor)

        up_text = TextZero()
        up_text.SetSize(const.TEXT_SIZE_SMALL)
        up_text.SetPosition(const.TEXT_POS_HCENTRE_UP)
        up_text.SetValue(values[2])
        renderer.AddActor(up_text.actor)

        down_text = TextZero()
        down_text.SetSize(const.TEXT_SIZE_SMALL)
        down_text.SetPosition(const.TEXT_POS_HCENTRE_DOWN_ZERO)
        down_text.SetValue(values[3])
        renderer.AddActor(down_text.actor)
    
    def get_coordinate_cursor(self, mx: int, my: int, orientation: str, picker: vtk.vtkWorldPointPicker) -> Tuple:
        if orientation == "AXIAL":
            slice_data = self.slice_data_axial
        elif orientation == "CORONAL":
            slice_data = self.slice_data_coronal
        else:
            slice_data = self.slice_data_sagital

        renderer = slice_data.renderer
        picker.Pick(mx, my, 0, renderer)
        x, y, z = picker.GetPickPosition()
        bounds = slice_data.actor.GetBounds()
        if bounds[0] == bounds[1]:
            x = bounds[0]
        elif bounds[2] == bounds[3]:
            y = bounds[2]
        elif bounds[4] == bounds[5]:
            z = bounds[4]
        return x, y, z
    
    def SetCrossFocalPoint(self, position: List) -> None:
        self.cross_axial.SetFocalPoint(position)
        self.cross_axial.Update()
        self.cross_axial.GetOutput().GetCellData().SetScalars(self.color_array_axial)
        
        self.cross_coronal.SetFocalPoint(position)
        self.cross_coronal.Update()
        self.cross_coronal.GetOutput().GetCellData().SetScalars(self.color_array_coronal)
        
        self.cross_sagital.SetFocalPoint(position)
        self.cross_sagital.Update()
        self.cross_sagital.GetOutput().GetCellData().SetScalars(self.color_array_sagital)

    def calculate_matrix_position(self, orientation: str, coord: Tuple) -> Tuple:
        x, y, z = coord
        if orientation == "AXIAL":
            xi, xf, yi, yf, zi, zf = self.slice_data_axial.actor.GetBounds()
            mx = round((x - xi) / self.slice.spacing[0], 0)
            my = round((y - yi) / self.slice.spacing[1], 0)
        elif orientation == "CORONAL":
            xi, xf, yi, yf, zi, zf = self.slice_data_coronal.actor.GetBounds()
            mx = round((x - xi) / self.slice.spacing[0], 0)
            my = round((z - zi) / self.slice.spacing[2], 0)
        elif orientation == "SAGITAL":
            xi, xf, yi, yf, zi, zf = self.slice_data_sagital.actor.GetBounds()
            mx = round((y - yi) / self.slice.spacing[1], 0)
            my = round((z - zi) / self.slice.spacing[2], 0)
        return int(mx), int(my)
    
    def get_slice_pixel_coord_by_world_pos(self, orientation: str, wx: float, wy: float, wz: float) -> Tuple:
        coord = (wx, wy, wz)
        px, py = self.calculate_matrix_position(orientation, coord)
        return px, py
    
    def calcultate_scroll_position(self, orientation: str, x: int, y: int) -> Tuple:
        # Based in the given coord (x, y), returns a list with the scroll positions for each
        # orientation, being the first position the sagital, second the coronal and the last, axial.
        if orientation == "AXIAL":
            axial = self.slice_data_axial.number
            coronal = y
            sagital = x
        elif orientation == "CORONAL":
            axial = y
            coronal = self.slice_data_coronal.number
            sagital = x
        elif orientation == "SAGITAL":
            axial = y
            coronal = x
            sagital = self.slice_data_sagital.number
        return sagital, coronal, axial
    
    def UpdateSlicesPosition(self, orientation: str, position: List) -> None:
        px, py = self.get_slice_pixel_coord_by_world_pos(orientation, *position)
        sagital, coronal, axial = self.calcultate_scroll_position(orientation, px, py)
        if orientation == "AXIAL":
            self.scroll_position_coronal = int(coronal)
            pos = self.scroll_position_coronal
            self.set_slice_number(pos, "CORONAL")

            self.scroll_position_sagital = int(sagital)
            pos = self.scroll_position_sagital
            self.set_slice_number(pos, "SAGITAL")
        elif orientation == "CORONAL":
            self.scroll_position_axial = int(axial)
            pos = self.scroll_position_axial
            self.set_slice_number(pos, "AXIAL")

            self.scroll_position_sagital = int(sagital)
            pos = self.scroll_position_sagital
            self.set_slice_number(pos, "SAGITAL")
        else:
            self.scroll_position_axial = int(axial)
            pos = self.scroll_position_axial
            self.set_slice_number(pos, "AXIAL")
            
            self.scroll_position_coronal = int(coronal)
            pos = self.scroll_position_coronal
            self.set_slice_number(coronal, "CORONAL")

    def UpdateSlice3D(self, orientations: List) -> None:
        for orientation in orientations:
            self.volume_viewer.slice_plane.ChangeSlice(orientation)

    def loadData(self) -> None:
        # 281
        path = "D:/workingspace/dicom/220277460 Nguyen Thanh Dat"
        # 289
        # path = "D:/workingspace/dicom/DICOM_NGUYEN VAN HUONG78T_CT_9210255004/1.2.392.200036.9123.100.11.12.700001708.2024010308030744.44/1.2.392.200036.9123.100.11.15114374081372786170424474122344997"
        # path = "D:/workingspace/viewer/be_project/viewer-core/server3d/src/data/2.25.308347458458694628345015586377307886637/1.3.12.2.1107.5.1.7.120165.30000024100716114480400000287/data"
        # path = "D:/workingspace/viewer/be_project/viewer-core/server3d/src/data/1.2.840.113619.2.438.3.2831208971.408.1719531439.122/1.2.840.113619.2.438.3.2831208971.408.1719531439.198/data"
        # path = "D:/workingspace/viewer/be_project/viewer-core/server3d/src/data/2.25.276674408816863868815262153252203392782/1.2.840.113619.2.428.3.678656.566.1723853367.555.3/data"
        dicomReader = vtk.vtkDICOMImageReader()
        dicomReader.SetDirectoryName(path)
        dicomReader.Update()
        imageData = dicomReader.GetOutput()

        slice = Slice()
        dimensions = imageData.GetDimensions()
        shape = dimensions[::-1]
        matrix = vtk_to_numpy(imageData.GetPointData().GetScalars()).reshape(shape)
        slice.matrix = matrix
        slice.spacing = imageData.GetSpacing()
        slice.center = imageData.GetCenter()

    def OnScrollForward(self, orientation: str) -> None:
        min = 0
        if orientation == "AXIAL":
            position = self.scroll_position_axial
        elif orientation == "CORONAL":
            position = self.scroll_position_coronal
        else:
            position = self.scroll_position_sagital

        if position >= min:
            position = position - 1
            self.set_slice_number(position, orientation)
            if orientation == "AXIAL":
                self.scroll_position_axial = position
                x, y, z = self.cross_axial.GetFocalPoint()
            elif orientation == "CORONAL":
                self.scroll_position_coronal = position
                x, y, z = self.cross_coronal.GetFocalPoint()
            else:
                self.scroll_position_sagital = position
                x, y, z = self.cross_sagital.GetFocalPoint()
            self.SetCrossFocalPoint([x, y, z])
            self.UpdateRender()
            # self.UpdateSlice3D([orientation])
            # render_window_volume = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
            # render_window_volume.Render()

    def OnScrollBackward(self, orientation: str) -> None:
        max = self.slice.GetMaxSliceNumber(orientation)
        if orientation == "AXIAL":
            position = self.scroll_position_axial
        elif orientation == "CORONAL":
            position = self.scroll_position_coronal
        else:
            position = self.scroll_position_sagital

        if position <= max:
            position = position + 1
            self.set_slice_number(position, orientation)
            if orientation == "AXIAL":
                self.scroll_position_axial = position
                x, y, z = self.cross_axial.GetFocalPoint()
            elif orientation == "CORONAL":
                self.scroll_position_coronal = position
                x, y, z = self.cross_coronal.GetFocalPoint()
            else:
                self.scroll_position_sagital = position
                x, y, z = self.cross_sagital.GetFocalPoint()
            self.SetCrossFocalPoint([x, y, z])
            self.UpdateRender()
            # self.UpdateSlice3D([orientation])
            # render_window_volume = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
            # render_window_volume.Render()
    
    def UpdateCameraPosition(self, position: List) -> None:
        render_window = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        renderer = render_window.GetRenderers().GetFirstRenderer()
        camera = renderer.GetActiveCamera()

        currentFocalPoint = camera.GetFocalPoint()
        temp = [position[i] - currentFocalPoint[i] for i in range(3)]
        camera.SetFocalPoint(position[0], position[1], position[2])

        currentCameraPosition = camera.GetPosition()
        camera.SetPosition([currentCameraPosition[i] + temp[i] for i in range(3)])
        
        renderer.ResetCameraClippingRange()
    
    @exportRpc("volume.create")
    def createVisualization(self, viewMode=None, size=None) -> None:
        # Load dicom
        self.loadData()

        self.slice_data_axial = self.create_slice_window("AXIAL")
        self.slice_data_coronal = self.create_slice_window("CORONAL")
        self.slice_data_sagital = self.create_slice_window("SAGITAL")

        self.build_cross_lines()

        # self.EnableText("AXIAL")
        # self.EnableText("CORONAL")
        # self.EnableText("SAGITAL")

        self.slice = Slice()

        position_axial = self.slice.GetNumberOfSlices("AXIAL") // 2
        self.scroll_position_axial = position_axial
        self.set_slice_number(position_axial, "AXIAL")

        position_coronal = self.slice.GetNumberOfSlices("CORONAL") // 2
        self.scroll_position_coronal = position_coronal
        self.set_slice_number(position_coronal, "CORONAL")

        position_sagital = self.slice.GetNumberOfSlices("SAGITAL") // 2
        self.scroll_position_sagital = position_sagital
        self.set_slice_number(position_sagital, "SAGITAL")

        self.update_camera("AXIAL")
        self.update_camera("CORONAL")
        self.update_camera("SAGITAL")

        render_window_axial = self.getApplication().GetObjectIdMap().GetActiveObject("AXIAL_VIEW")
        render_window_axial.Render()

        render_window_coronal = self.getApplication().GetObjectIdMap().GetActiveObject("CORONAL_VIEW")
        render_window_coronal.Render()

        render_window_sagital = self.getApplication().GetObjectIdMap().GetActiveObject("SAGITAL_VIEW")
        render_window_sagital.Render()

        self.SetInteractorStyle()

        volume_viewer = self.volume_viewer = VolumeViewer()
        volume_viewer.LoadVolume()

        render_window_volume = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        renderer_volume = render_window_volume.GetRenderers().GetFirstRenderer()
        renderer_volume.AddVolume(volume_viewer.volume)
        renderer_volume.ResetCamera()

        # volume_viewer.LoadSlicePlane()
        # slice_plane = volume_viewer.slice_plane
        # slice_plane.UpdateAllSlice()

        # interactor_volume = render_window_volume.GetInteractor()
        # slice_plane.plane_z.SetInteractor(interactor_volume)
        # slice_plane.plane_y.SetInteractor(interactor_volume)
        # slice_plane.plane_x.SetInteractor(interactor_volume)
        # slice_plane.Enable()

        render_window_volume.Render()

        # endo_viewer = self.endo_viewer = EndoscopyViewer()
        # endo_viewer.LoadVolume()

        # render_window_volume = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        # renderer_volume = render_window_volume.GetRenderers().GetFirstRenderer()
        # renderer_volume.AddVolume(endo_viewer.volume)
        # renderer_volume.ResetCamera()

        # camera = renderer_volume.GetActiveCamera()
        # camera.SetViewUp(0, 1, 0)
        # center = endo_viewer.volume.GetCenter()
        # camera.SetFocalPoint(center[0], center[1], center[2])
        # camera.SetPosition(center[0], center[1], center[2] + 5)
        # camera.SetViewAngle(90)

        # render_window_volume.Render()
    
    @exportRpc("viewport.mouse.zoom.wheel")
    def updateZoomFromWheel(self, event) -> None:
        if 'Start' in event["type"]:
            self.getApplication().InvokeEvent(vtk.vtkCommand.StartInteractionEvent)

        viewId = event["view"]
        # Volume
        if viewId == "1":
            render_window_volume = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
            if render_window_volume and 'spinY' in event:
                zoomFactor = 1.0 - event['spinY'] / 10.0

                camera = render_window_volume.GetRenderers().GetFirstRenderer().GetActiveCamera()
                fp = camera.GetFocalPoint()
                pos = camera.GetPosition()
                delta = [fp[i] - pos[i] for i in range(3)]
                camera.Zoom(zoomFactor)

                pos2 = camera.GetPosition()
                camera.SetFocalPoint([pos2[i] + delta[i] for i in range(3)])
                render_window_volume.Modified()
        # Axial
        elif viewId == "2":
            if "spinY" in event and event.get("spinY") and event.get("spinY") < 0:
                self.OnScrollForward("AXIAL")
            elif "spinY" in event and event.get("spinY") and event.get("spinY") > 0:
                self.OnScrollBackward("AXIAL")
        # Coronal
        elif viewId == "3":
            if "spinY" in event and event.get("spinY") and event.get("spinY") < 0:
                self.OnScrollForward("CORONAL")
            elif "spinY" in event and event.get("spinY") and event.get("spinY") > 0:
                self.OnScrollBackward("CORONAL")
        # Sagital
        elif viewId == "4":
            if "spinY" in event and event.get("spinY") and event.get("spinY") < 0:
                self.OnScrollForward("SAGITAL")
            elif "spinY" in event and event.get("spinY") and event.get("spinY") > 0:
                self.OnScrollBackward("SAGITAL")

        if 'End' in event["type"]:
            self.getApplication().InvokeEvent(vtk.vtkCommand.EndInteractionEvent)

    # @exportRpc("viewport.mouse.interaction")
    def mouseInteraction(self, event):
        """
        RPC Callback for mouse interactions.
        """
        view = self.getView(event["view"])

        orientation = None
        if event["view"] == '1':
            orientation = "VOLUME"
        elif event["view"] == '2':
            orientation = "AXIAL"
        elif event["view"] == '3':
            orientation = "CORONAL"
        else:
            orientation = "SAGITAL"

        buttons = 0
        if event["buttonLeft"]:
            buttons = vtk.vtkWebInteractionEvent.LEFT_BUTTON
        if event["buttonMiddle"]:
            buttons = vtk.vtkWebInteractionEvent.MIDDLE_BUTTON
        if event["buttonRight"]:
            buttons = vtk.vtkWebInteractionEvent.RIGHT_BUTTON

        modifiers = 0
        if event["shiftKey"]:
            modifiers = vtk.vtkWebInteractionEvent.SHIFT_KEY
        if event["ctrlKey"]:
            modifiers = vtk.vtkWebInteractionEvent.CTRL_KEY
        if event["altKey"]:
            modifiers = vtk.vtkWebInteractionEvent.ALT_KEY
        if event["metaKey"]:
            modifiers = vtk.vtkWebInteractionEvent.META_KEY

        pvevent = vtk.vtkWebInteractionEvent()
        pvevent.SetButtons(buttons)
        pvevent.SetModifiers(modifiers)
        if "x" in event:
            pvevent.SetX(event["x"])
        if "y" in event:
            pvevent.SetY(event["y"])
        if "scroll" in event:
            pvevent.SetScroll(event["scroll"])
        if event["action"] == "dblclick":
            pvevent.SetRepeatCount(2)
        # pvevent.SetKeyCode(event["charCode"])
        retVal = self.getApplication().HandleInteractionEvent(view, pvevent)
        del pvevent

        if event["action"] == "down":
            self.getApplication().InvokeEvent("StartInteractionEvent")
            if event["buttonLeft"]:
                if orientation == 'VOLUME':
                    # # Start rotate
                    # # view.GetInteractor().GetInteractorStyle().StartRotate()

                    # # Rotate
                    # renderer = view.GetRenderers().GetFirstRenderer()

                    # last_position = view.GetInteractor().GetLastEventPosition()
                    # # print(f"last position: {last_position}")
                    # position = view.GetInteractor().GetEventPosition()
                    # # print(f"position: {position}")
                    # dx = position[0] - last_position[0]
                    # dy = position[1] - last_position[1]

                    # size = view.GetSize()

                    # delta_elevation = -20.0 / size[1]
                    # delta_azimuth = -20.0 / size[0]

                    # MotionFactor = 10.0
                    # rxf = dx * delta_azimuth * MotionFactor
                    # ryf = dy * delta_elevation * MotionFactor

                    # camera = renderer.GetActiveCamera()
                    # camera.Azimuth(rxf)
                    # # print(f"Azimuth: {rxf}")
                    # camera.Elevation(ryf)
                    # # print(f"Elevation: {ryf}")
                    # camera.OrthogonalizeViewUp()

                    # view.Render()
                    pass
                else:
                    size = view.GetSize()
                    mouse_x = round(event["x"] * size[0])
                    mouse_y = round(event["y"] * size[1])
                    # mouse_x, mouse_y = view.GetInteractor().GetEventPosition()
                    x, y, z = self.get_coordinate_cursor(mouse_x, mouse_y, orientation, self.picker)
                    self.UpdateSlicesPosition(orientation, [x, y, z])
                    self.SetCrossFocalPoint([x, y, z])
                    self.UpdateRender(orientation)

        if event["action"] == "up":
            self.getApplication().InvokeEvent("EndInteractionEvent")

        if retVal:
            self.getApplication().InvokeEvent("UpdateEvent")

        return retVal
    
    @exportRpc("endoscopy.flythrough.revert")
    def revert(self) -> None:
        # render_window = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        render_window = self.getView('4')
        renderer = render_window.GetRenderers().GetFirstRenderer()

        camera = renderer.GetActiveCamera()
        camera.Azimuth(180)

        render_window.Render()
        self.getApplication().InvokeEvent(vtk.vtkCommand.UpdateEvent)

    @exportRpc("endoscopy.flythrough.prev")
    def prev(self) -> None:
        orientation = "AXIAL"
        self.OnScrollBackward(orientation)

        position = self.cross_axial.GetFocalPoint()
        self.UpdateCameraPosition(position)

        # render_window = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        render_window = self.getView('4')
        render_window.Render()
        self.getApplication().InvokeEvent(vtk.vtkCommand.UpdateEvent)

    @exportRpc("endoscopy.flythrough.next")
    def next(self) -> None:
        orientation = "AXIAL"
        self.OnScrollForward(orientation)

        position = self.cross_axial.GetFocalPoint()
        self.UpdateCameraPosition(position)

        # render_window = self.getApplication().GetObjectIdMap().GetActiveObject("VOLUME_VIEW")
        render_window = self.getView('4')
        render_window.Render()
        self.getApplication().InvokeEvent(vtk.vtkCommand.UpdateEvent)
