import math, logging, time

from typing import Union, List, Tuple

from wslink import register as exportRpc

import vtk
from vtk.web import protocols as vtk_protocols
from vtkmodules.vtkCommonCore import vtkCommand

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

vtkmath = vtk.vtkMath()

class Viewer(vtk_protocols.vtkWebProtocol):
    def __init__(self):
        self.dicomDirPath = "D:/javaworkspace/viewer-core/server3d/data/1.2.840.113704.9.1000.16.0.20240527133901371/1.2.840.113704.9.1000.16.1.2024052713392627100020002/data"
        self.colors = vtk.vtkNamedColors()

        self.initialize()

        self.initCenterlineAxialView()
        self.initCenterlineCoronalView()
        self.initCenterlineSagittalView()

        self.initWidgetsAxialView()
        self.initWidgetsCoronalView()
        self.initWidgetsSagittalView()

        # Used to save current position
        self.currentSphereWidgetCenter = None
        self.currentSphereWidgetCenterRotateLinesAxial = None

    def initialize(self) -> None:
        self.reader = vtk.vtkDICOMImageReader()
        self.axial = vtk.vtkMatrix4x4()
        self.coronal = vtk.vtkMatrix4x4()
        self.sagittal = vtk.vtkMatrix4x4()
        self.rotationMatrix = vtk.vtkMatrix4x4()
        self.resultMatrix = vtk.vtkMatrix4x4()
        self.resliceAxial = vtk.vtkImageReslice()
        self.resliceCoronal = vtk.vtkImageReslice()
        self.resliceSagittal = vtk.vtkImageReslice()
        self.actorAxial = vtk.vtkImageActor()
        self.actorCoronal = vtk.vtkImageActor()
        self.actorSagittal = vtk.vtkImageActor()
        self.cameraAxialView = vtk.vtkCamera()
        self.cameraCoronalView = vtk.vtkCamera()
        self.cameraSagittalView = vtk.vtkCamera()
        self.rendererAxial = vtk.vtkRenderer()
        self.rendererCoronal = vtk.vtkRenderer()
        self.rendererSagittal = vtk.vtkRenderer()

        self.rendererAxial.SetBackground(0.3, 0.1, 0.1)
        self.rendererCoronal.SetBackground(0.1, 0.3, 0.1)
        self.rendererSagittal.SetBackground(0.1, 0.1, 0.3)

        # Initialize rotation matrix (y-axes)
        self.rotationMatrix.DeepCopy(
            (math.cos(math.radians(0)), 0, math.sin(math.radians(0)), 0, 
            0, 1, 0, 0, 
            -math.sin(math.radians(0)), 0, math.cos(math.radians(0)), 0, 
            0, 0, 0, 1)
        )

        # 3D view
        self.mapper = vtk.vtkSmartVolumeMapper()
        self.volumeProperty = vtk.vtkVolumeProperty()
        self.volume = vtk.vtkVolume()
        # Transfer function
        self.scalarColorTransferFunction = vtk.vtkColorTransferFunction()
        self.scalarOpacity = vtk.vtkPiecewiseFunction()
        self.gradientOpacity = vtk.vtkPiecewiseFunction()

    def initCenterlineAxialView(self) -> None:
        greenLineAxial = vtk.vtkLineSource()
        greenLineAxial.SetPoint1(0, 500, 0)
        greenLineAxial.SetPoint2(0, -500, 0)
        greenLineAxial.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(greenLineAxial.GetOutput().GetNumberOfCells())
        for c in range(greenLineAxial.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 255, 0])
        greenLineAxial.GetOutput().GetCellData().SetScalars(colorArray)

        blueLineAxial = vtk.vtkLineSource()
        blueLineAxial.SetPoint1(-500, 0, 0)
        blueLineAxial.SetPoint2(500, 0, 0)
        blueLineAxial.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(blueLineAxial.GetOutput().GetNumberOfCells())
        for c in range(blueLineAxial.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 0, 255])
        blueLineAxial.GetOutput().GetCellData().SetScalars(colorArray)

        linesAxial = vtk.vtkAppendPolyData()
        linesAxial.AddInputData(greenLineAxial.GetOutput())
        linesAxial.AddInputData(blueLineAxial.GetOutput())
        linesAxial.Update()

        linesAxialMapper = vtk.vtkPolyDataMapper()
        linesAxialMapper.SetInputConnection(linesAxial.GetOutputPort())

        self.linesAxialActor = vtk.vtkActor()
        self.linesAxialActor.SetMapper(linesAxialMapper)
        self.linesAxialActor.GetProperty().SetLineWidth(1)
        self.linesAxialActor.SetOrigin(0, 0, 0)
        
    def initCenterlineCoronalView(self) -> None:
        greenLineCoronal = vtk.vtkLineSource()
        greenLineCoronal.SetPoint1(0, 0, -500)
        greenLineCoronal.SetPoint2(0, 0, 500)
        greenLineCoronal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(greenLineCoronal.GetOutput().GetNumberOfCells())
        for c in range(greenLineCoronal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 255, 0])
        greenLineCoronal.GetOutput().GetCellData().SetScalars(colorArray)

        redLineCoronal = vtk.vtkLineSource()
        redLineCoronal.SetPoint1(-500, 0, 0)
        redLineCoronal.SetPoint2(500, 0, 0)
        redLineCoronal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(redLineCoronal.GetOutput().GetNumberOfCells())
        for c in range(redLineCoronal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [255, 0, 0])
        redLineCoronal.GetOutput().GetCellData().SetScalars(colorArray)

        linesCoronal = vtk.vtkAppendPolyData()
        linesCoronal.AddInputData(greenLineCoronal.GetOutput())
        linesCoronal.AddInputData(redLineCoronal.GetOutput())
        linesCoronal.Update()

        linesCoronalMapper = vtk.vtkPolyDataMapper()
        linesCoronalMapper.SetInputConnection(linesCoronal.GetOutputPort())

        self.linesCoronalActor = vtk.vtkActor()
        self.linesCoronalActor.SetMapper(linesCoronalMapper)
        self.linesCoronalActor.GetProperty().SetLineWidth(1)
        self.linesCoronalActor.SetOrigin(0, 0, 0)

    def initCenterlineSagittalView(self) -> None:
        blueLineSagittal = vtk.vtkLineSource()
        blueLineSagittal.SetPoint1(0, 0, -500)
        blueLineSagittal.SetPoint2(0, 0, 500)
        blueLineSagittal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(blueLineSagittal.GetOutput().GetNumberOfCells())
        for c in range(blueLineSagittal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 0, 255])
        blueLineSagittal.GetOutput().GetCellData().SetScalars(colorArray)

        redLineSagittal = vtk.vtkLineSource()
        redLineSagittal.SetPoint1(0, -500, 0)
        redLineSagittal.SetPoint2(0, 500, 0)
        redLineSagittal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(redLineSagittal.GetOutput().GetNumberOfCells())
        for c in range(redLineSagittal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [255, 0, 0])
        redLineSagittal.GetOutput().GetCellData().SetScalars(colorArray)

        linesSagittal = vtk.vtkAppendPolyData()
        linesSagittal.AddInputData(blueLineSagittal.GetOutput())
        linesSagittal.AddInputData(redLineSagittal.GetOutput())
        linesSagittal.Update()

        linesSagittalMapper = vtk.vtkPolyDataMapper()
        linesSagittalMapper.SetInputConnection(linesSagittal.GetOutputPort())

        self.linesSagittalActor = vtk.vtkActor()
        self.linesSagittalActor.SetMapper(linesSagittalMapper)
        self.linesSagittalActor.GetProperty().SetLineWidth(1)
        self.linesSagittalActor.SetOrigin(0, 0, 0)

    def initWidgetsAxialView(self) -> None:
        self.sphereWidgetAxial = vtk.vtkSphereWidget()
        self.sphereWidgetAxial.SetRadius(5)
        self.sphereWidgetAxial.SetRepresentationToSurface()
        self.sphereWidgetAxial.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        self.sphereWidgetAxial.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetAxial.SetCurrentRenderer(self.rendererAxial)

        # self.sphereWidgetInteractionRotateGreenLineAxial = vtk.vtkSphereWidget()
        # self.sphereWidgetInteractionRotateGreenLineAxial.SetRadius(5)
        # self.sphereWidgetInteractionRotateGreenLineAxial.SetRepresentationToSurface()
        # self.sphereWidgetInteractionRotateGreenLineAxial.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        # self.sphereWidgetInteractionRotateGreenLineAxial.GetSelectedSphereProperty().SetOpacity(0)
        # self.sphereWidgetInteractionRotateGreenLineAxial.SetCurrentRenderer(self.rendererAxial)

    def initWidgetsCoronalView(self) -> None:
        self.sphereWidgetCoronal = vtk.vtkSphereWidget()
        self.sphereWidgetCoronal.SetRadius(5)
        self.sphereWidgetCoronal.SetRepresentationToSurface()
        self.sphereWidgetCoronal.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        self.sphereWidgetCoronal.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetCoronal.SetCurrentRenderer(self.rendererCoronal)

    def initWidgetsSagittalView(self) -> None:
        self.sphereWidgetSagittal = vtk.vtkSphereWidget()
        self.sphereWidgetSagittal.SetRadius(5)
        self.sphereWidgetSagittal.SetRepresentationToSurface()
        self.sphereWidgetSagittal.GetSphereProperty().SetColor(self.colors.GetColor3d("Blue"))
        self.sphereWidgetSagittal.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetSagittal.SetCurrentRenderer(self.rendererSagittal)

    def turnOnWidgets(self) -> None:
        self.sphereWidgetAxial.On()
        # self.sphereWidgetInteractionRotateGreenLineAxial.On()
        self.sphereWidgetCoronal.On()
        self.sphereWidgetSagittal.On()

    def turnOffWidgets(self) -> None:
        self.sphereWidgetAxial.Off()
        # self.sphereWidgetInteractionRotateGreenLineAxial.Off()
        self.sphereWidgetCoronal.Off()
        self.sphereWidgetSagittal.Off()

    def setCrosshairPositionAxialView(self, position: Union[List, Tuple]) -> None:
        self.sphereWidgetAxial.SetCenter(position)
        self.linesAxialActor.SetPosition(position)

    def setCrosshairPositionCoronalView(self, position: Union[List, Tuple]) -> None:
        self.sphereWidgetCoronal.SetCenter(position)
        self.linesCoronalActor.SetPosition(position)

    def setCrosshairPositionSagittalView(self, position: Union[List, Tuple]) -> None:
        self.sphereWidgetSagittal.SetCenter(position)
        self.linesSagittalActor.SetPosition(position)

    def apply3DPreset(self) -> None:
        self.volumeProperty.SetAmbient(0.1)
        self.volumeProperty.SetDiffuse(0.9)
        self.volumeProperty.SetSpecular(0.2)
        self.volumeProperty.SetSpecularPower(10)
        
        self.volumeProperty.ShadeOn()

        self.scalarColorTransferFunction.AddRGBPoint(-3024, 0, 0, 0)
        self.scalarColorTransferFunction.AddRGBPoint(143.56, 157/255, 91/255, 47/255)
        self.scalarColorTransferFunction.AddRGBPoint(166.22, 225/255, 154/255, 74/255)
        self.scalarColorTransferFunction.AddRGBPoint(214.39, 255/255, 255/255, 255/255)
        self.scalarColorTransferFunction.AddRGBPoint(419.74, 255/255, 239/255, 243/255)
        self.scalarColorTransferFunction.AddRGBPoint(3071, 211/255, 168/255, 255/255)

        self.scalarOpacity.AddPoint(-3024, 0)
        self.scalarOpacity.AddPoint(143.56, 0)
        self.scalarOpacity.AddPoint(166.22, 0.69)
        self.scalarOpacity.AddPoint(214.39, 0.7)
        self.scalarOpacity.AddPoint(3071, 0.8)

        self.gradientOpacity.AddPoint(0, 0)
        self.gradientOpacity.AddPoint(255, 1)

    @exportRpc("volume.initialize")
    def createVisualization(self) -> None:
        renderWindowAxial = self.getApplication().GetObjectIdMap().GetActiveObject("AXIAL_VIEW")
        renderWindowCoronal = self.getApplication().GetObjectIdMap().GetActiveObject("CORONAL_VIEW")
        renderWindowSagittal = self.getApplication().GetObjectIdMap().GetActiveObject("SAGITTAL_VIEW")
        renderWindow = self.getApplication().GetObjectIdMap().GetActiveObject("3D_VIEW")

        # Reader
        self.reader.SetDirectoryName(self.dicomDirPath)
        self.reader.Update()
        imageData = self.reader.GetOutput()
        center = imageData.GetCenter()
        (xMin, xMax, yMin, yMax, zMin, zMax) = imageData.GetBounds()

        # 3D
        self.mapper.SetInputData(imageData)
        self.volumeProperty.SetInterpolationTypeToLinear()
        self.volumeProperty.SetScalarOpacityUnitDistance(0.1)
        self.volumeProperty.SetColor(self.scalarColorTransferFunction)
        self.volumeProperty.SetScalarOpacity(self.scalarOpacity)
        self.volumeProperty.SetGradientOpacity(self.gradientOpacity)
        self.apply3DPreset()
        self.volume.SetMapper(self.mapper)
        self.volume.SetProperty(self.volumeProperty)
        renderer = renderWindow.GetRenderers().GetFirstRenderer()
        renderer.AddVolume(self.volume)

        self.sphereWidgetAxial.SetInteractor(renderWindowAxial.GetInteractor())
        # self.sphereWidgetInteractionRotateGreenLineAxial.SetInteractor(renderWindowAxial.GetInteractor())
        self.sphereWidgetCoronal.SetInteractor(renderWindowCoronal.GetInteractor())
        self.sphereWidgetSagittal.SetInteractor(renderWindowSagittal.GetInteractor())

        # Set crosshair position in views
        self.setCrosshairPositionAxialView(center)
        self.setCrosshairPositionCoronalView(center)
        self.setCrosshairPositionSagittalView(center)

        # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter(center[0], (yMax + center[1])/2, center[2])

        # Matrices for axial, coronal, and sagittal view orientations
        # Model matrix = Translation matrix
        self.axial.DeepCopy(
            (1, 0, 0, center[0],
            0, 1, 0, center[1],
            0, 0, 1, center[2],
            0, 0, 0, 1)
        )
        # Model matrix = Translation matrix . Rotation matrix x-axes(90)
        self.coronal.DeepCopy(
            (1, 0, 0, center[0],
            0, 0, 1, center[1],
            0, -1, 0, center[2],
            0, 0, 0, 1)
        )
        # Model matrix = Translation matrix . Rotation matrix x-axes(90) . Rotation matrix y-axes(90)
        self.sagittal.DeepCopy(
            (0, 0, -1, center[0],
            1, 0, 0, center[1],
            0, -1, 0, center[2],
            0, 0, 0, 1)
        )

        # Extract a slice in the desired orientation
        self.resliceAxial.SetInputData(imageData)
        self.resliceAxial.SetOutputDimensionality(2)
        self.resliceAxial.SetResliceAxes(self.axial)
        self.resliceAxial.SetInterpolationModeToLinear()

        self.resliceCoronal.SetInputData(imageData)
        self.resliceCoronal.SetOutputDimensionality(2)
        self.resliceCoronal.SetResliceAxes(self.coronal)
        self.resliceCoronal.SetInterpolationModeToLinear()
        
        self.resliceSagittal.SetInputData(imageData)
        self.resliceSagittal.SetOutputDimensionality(2)
        self.resliceSagittal.SetResliceAxes(self.sagittal)
        self.resliceSagittal.SetInterpolationModeToLinear()

        # Display
        self.actorAxial.GetMapper().SetInputConnection(self.resliceAxial.GetOutputPort())
        self.actorCoronal.GetMapper().SetInputConnection(self.resliceCoronal.GetOutputPort())
        self.actorSagittal.GetMapper().SetInputConnection(self.resliceSagittal.GetOutputPort())

        # Set position and rotate in world coordinates
        self.actorAxial.SetUserMatrix(self.axial)
        self.actorCoronal.SetUserMatrix(self.coronal)
        self.actorSagittal.SetUserMatrix(self.sagittal)

        # Set renderers
        self.rendererAxial.AddActor(self.actorAxial)
        self.rendererAxial.AddActor(self.linesAxialActor)
        # The reset camera call is figuring out the frustum bounds based on all the actors present
        # in the viewport.
        self.rendererAxial.ResetCamera()
        self.cameraAxialView.SetPosition(center[0], center[1], 2*zMax)
        self.cameraAxialView.SetFocalPoint(center)
        self.cameraAxialView.SetViewUp(0, 1, 0)
        self.cameraAxialView.SetThickness(2*zMax)
        self.rendererAxial.SetActiveCamera(self.cameraAxialView)

        self.rendererCoronal.AddActor(self.actorCoronal)
        self.rendererCoronal.AddActor(self.linesCoronalActor)
        # The reset camera call is figuring out the frustum bounds based on all the actors present
        # in the viewport.
        self.rendererCoronal.ResetCamera()
        self.cameraCoronalView.SetPosition(center[0], 2*yMax, center[2])
        self.cameraCoronalView.SetFocalPoint(center)
        self.cameraCoronalView.SetViewUp(0, 0, -1)
        self.cameraCoronalView.SetThickness(2*yMax)
        self.rendererCoronal.SetActiveCamera(self.cameraCoronalView)

        self.rendererSagittal.AddActor(self.actorSagittal)
        self.rendererSagittal.AddActor(self.linesSagittalActor)
        # The reset camera call is figuring out the frustum bounds based on all the actors present
        # in the viewport.
        self.rendererSagittal.ResetCamera()
        self.cameraSagittalView.SetPosition(2*xMax, center[1], center[2])
        self.cameraSagittalView.SetFocalPoint(center)
        self.cameraSagittalView.SetViewUp(0, 0, -1)
        self.cameraSagittalView.SetThickness(2*xMax)
        self.rendererSagittal.SetActiveCamera(self.cameraSagittalView)

        renderWindowAxial.AddRenderer(self.rendererAxial)
        renderWindowCoronal.AddRenderer(self.rendererCoronal)
        renderWindowSagittal.AddRenderer(self.rendererSagittal)

        # Create callback function for sphere widget interaction
        self.currentSphereWidgetCenter = {
            "axial": self.sphereWidgetAxial.GetCenter(),
            "coronal": self.sphereWidgetCoronal.GetCenter(),
            "sagittal": self.sphereWidgetSagittal.GetCenter()
        }
        # self.currentSphereWidgetCenterRotateLinesAxial = {
        #     "green": self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
        # }

        def setupCameraAxialView(newPosition: Union[List, Tuple]) -> None:
            cameraPosition = self.rendererAxial.GetActiveCamera().GetPosition()
            focalPoint = self.rendererAxial.GetActiveCamera().GetFocalPoint()
            reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
            normReverseProjectionVector = vtkmath.Norm(reverseProjectionVector)
            vector = [newPosition[i] - focalPoint[i] for i in range(3)]
            translationInterval = [(vtkmath.Dot(reverseProjectionVector, vector)/math.pow(normReverseProjectionVector, 2))*reverseProjectionVector[i] for i in range(3)]
            self.rendererAxial.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            self.rendererAxial.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

        def setupCameraCoronalView(newPosition: Union[List, Tuple]) -> None:
            cameraPosition = self.rendererCoronal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererCoronal.GetActiveCamera().GetFocalPoint()
            reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
            normReverseProjectionVector = vtkmath.Norm(reverseProjectionVector)
            vector = [newPosition[i] - focalPoint[i] for i in range(3)]
            translationInterval = [(vtkmath.Dot(reverseProjectionVector, vector)/math.pow(normReverseProjectionVector, 2))*reverseProjectionVector[i] for i in range(3)]
            self.rendererCoronal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            self.rendererCoronal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

        def setupCameraSagittalView(newPosition: Union[List, Tuple]) -> None:
            cameraPosition = self.rendererSagittal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererSagittal.GetActiveCamera().GetFocalPoint()
            reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
            normReverseProjectionVector = vtkmath.Norm(reverseProjectionVector)
            vector = [newPosition[i] - focalPoint[i] for i in range(3)]
            translationInterval = [(vtkmath.Dot(reverseProjectionVector, vector)/math.pow(normReverseProjectionVector, 2))*reverseProjectionVector[i] for i in range(3)]
            self.rendererSagittal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            self.rendererSagittal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

        def interactionEventHandleTranslateLinesAxialView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Set centerline position in axial view
            self.linesAxialActor.SetPosition(newPosition)
            # Set rotation position on green line in axial view
            # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
            # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Extract image with new position
            self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)
            # Setup camera in coronal view
            setupCameraCoronalView(newPosition)

            # Extract image with new position
            self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)
            # Setup camera in sagittal view
            setupCameraSagittalView(newPosition)

            self.currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
            self.currentSphereWidgetCenter["sagittal"] = self.sphereWidgetCoronal.GetCenter()
            self.currentSphereWidgetCenter["coronal"] = self.sphereWidgetSagittal.GetCenter()

            renderWindowCoronal.Render()
            renderWindowSagittal.Render()

        def interactionEventHandleTranslateLinesCoronalView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Set centerline position in coronal view
            self.linesCoronalActor.SetPosition(newPosition)

            # Extract image with new position
            self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
            # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            # Setup camera in axial view
            setupCameraAxialView(newPosition)

            # Extract image with new position
            self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)
            # Setup camera in sagittal view
            setupCameraSagittalView(newPosition)

            self.currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
            self.currentSphereWidgetCenter["sagittal"] = self.sphereWidgetCoronal.GetCenter()
            self.currentSphereWidgetCenter["coronal"] = self.sphereWidgetSagittal.GetCenter()

            renderWindowAxial.Render()
            renderWindowSagittal.Render()

        def interactionEventHandleTranslateLinesSagittalView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Set centerline position in sagittal view
            self.linesSagittalActor.SetPosition(newPosition)

            # Extract image with new position
            self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["sagittal"][i] for i in range(3)]
            # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            # Setup camera in axial view
            setupCameraAxialView(newPosition)

            # Extract image with new position
            self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)
            # Setup camera in coronal view
            setupCameraCoronalView(newPosition)

            self.currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
            self.currentSphereWidgetCenter["sagittal"] = self.sphereWidgetCoronal.GetCenter()
            self.currentSphereWidgetCenter["coronal"] = self.sphereWidgetSagittal.GetCenter()

            renderWindowAxial.Render()
            renderWindowCoronal.Render()

        def interactionEventHandleRotateGreenLineAxialView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Calculate rotation angle (degree unit)
            v1 = [self.currentSphereWidgetCenterRotateLinesAxial["green"][i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
            v2 = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
            angle = vtkmath.DegreesFromRadians(vtkmath.SignedAngleBetweenVectors(v1, v2, [0, 0, -1]))
            # Rotate lines in axial view
            self.linesAxialActor.RotateZ(-angle)

            # Set elements of rotation matrix (y-axes)
            self.rotationMatrix.SetElement(0, 0, math.cos(math.radians(angle)))
            self.rotationMatrix.SetElement(0, 2, math.sin(math.radians(angle)))
            self.rotationMatrix.SetElement(2, 0, -math.sin(math.radians(angle)))
            self.rotationMatrix.SetElement(2, 2, math.cos(math.radians(angle)))
            
            # Calculate new transform matrix (sagittal view)
            vtk.vtkMatrix4x4.Multiply4x4(self.resliceSagittal.GetResliceAxes(), self.rotationMatrix, self.resultMatrix)
            # Extract image after rotation
            for i in range(4):
                for j in range(4):
                    self.resliceSagittal.GetResliceAxes().SetElement(i, j, self.resultMatrix.GetElement(i, j))
            self.linesSagittalActor.RotateZ(-angle)
            self.rendererSagittal.GetActiveCamera().Azimuth(angle)

            # Calculate new transform matrix (coronal view)
            vtk.vtkMatrix4x4.Multiply4x4(self.resliceCoronal.GetResliceAxes(), self.rotationMatrix, self.resultMatrix)
            # Extract image after rotation
            for i in range(4):
                for j in range(4):
                    self.resliceCoronal.GetResliceAxes().SetElement(i, j, self.resultMatrix.GetElement(i, j))
            self.linesCoronalActor.RotateZ(-angle)
            self.rendererCoronal.GetActiveCamera().Azimuth(angle)

            self.currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition

            renderWindowCoronal.Render()
            renderWindowSagittal.Render()
        
        self.sphereWidgetAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLinesAxialView)
        # self.sphereWidgetInteractionRotateGreenLineAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleRotateGreenLineAxialView)
        
        self.sphereWidgetCoronal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLinesCoronalView)
        
        self.sphereWidgetSagittal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLinesSagittalView)

        # Turn on sphere widget
        self.turnOnWidgets()

        renderWindowAxial.Render()
        renderWindowCoronal.Render()
        renderWindowSagittal.Render()
        renderWindow.Render()

        self.getApplication().InvalidateCache(renderWindowAxial)
        self.getApplication().InvalidateCache(renderWindowCoronal)
        self.getApplication().InvalidateCache(renderWindowSagittal)
        self.getApplication().InvalidateCache(renderWindow)

        self.getApplication().InvokeEvent(vtkCommand.UpdateEvent)

    @exportRpc("viewport.mouse.zoom.wheel")
    def updateZoomFromWheel(self, event):
        if 'Start' in event["type"]:
            self.getApplication().InvokeEvent(vtkCommand.StartInteractionEvent)
        # MouseWheelForwardEvent: event["spinY"] < 0
        # MouseWheelBackwardEvent: event["spinY"] > 0
        viewId = int(event.get("view"))
        # Axial view
        if viewId == 1:
            sliceSpacing = self.resliceAxial.GetOutput().GetSpacing()[2]
            cameraPosition = self.rendererAxial.GetActiveCamera().GetPosition()
            focalPoint = self.rendererAxial.GetActiveCamera().GetFocalPoint()

            if "spinY" in event and event.get("spinY") and event.get("spinY") < 0:
                # Move the center point that we are slicing through
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                normProjectionVector = vtk.vtkMath.Norm(projectionVector)
                translationInterval = [(sliceSpacing/normProjectionVector) * projectionVector[i] for i in range(3)]
                newPosition = [self.currentSphereWidgetCenter["axial"][i] + translationInterval[i] for i in range(3)]
                self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])

                # Set crosshair position in axial view
                self.setCrosshairPositionAxialView(newPosition)
                # Set rotation position on green line in axial view
                # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
                # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
                # Setup camera in axial view
                self.rendererAxial.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
                self.rendererAxial.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

                # Set crosshair position in coronal view
                self.setCrosshairPositionCoronalView(newPosition)

                # Set crosshair position in sagittal view
                self.setCrosshairPositionSagittalView(newPosition)

            elif "spinY" in event and event.get("spinY") and event.get("spinY") > 0:
                # Move the center point that we are slicing through
                reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                normReverseProjectionVector = vtk.vtkMath.Norm(reverseProjectionVector)
                translationInterval = [(sliceSpacing/normReverseProjectionVector) * reverseProjectionVector[i] for i in range(3)]
                newPosition = [self.currentSphereWidgetCenter["axial"][i] + translationInterval[i] for i in range(3)]
                self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])

                # Set crosshair position in axial view
                self.setCrosshairPositionAxialView(newPosition)
                # Set rotation position on green line in axial view
                # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
                # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
                # Setup camera in axial view
                self.rendererAxial.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
                self.rendererAxial.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

                # Set crosshair position in coronal view
                self.setCrosshairPositionCoronalView(newPosition)

                # Set crosshair position in sagittal view
                self.setCrosshairPositionSagittalView(newPosition)

        # Coronal view
        elif viewId == 2:
            sliceSpacing = self.resliceCoronal.GetOutput().GetSpacing()[2]
            cameraPosition = self.rendererCoronal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererCoronal.GetActiveCamera().GetFocalPoint()

            if "spinY" in event and event["spinY"] and event["spinY"] < 0:
                # Move the center point that we are slicing through
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                translationInterval = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [self.currentSphereWidgetCenter["coronal"][i] + translationInterval[i] for i in range(3)]
                self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])

                # Set crosshair position in coronal view
                self.setCrosshairPositionCoronalView(newPosition)
                # Set camera position in coronal view
                self.rendererCoronal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
                self.rendererCoronal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

                # Set crosshair position in axial view
                self.setCrosshairPositionAxialView(newPosition)
                # Set rotation position on green line in axial view
                # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
                # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
                # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
                
                # Set crosshair position in sagittal view
                self.setCrosshairPositionSagittalView(newPosition)

            elif "spinY" in event and event["spinY"] and event["spinY"] > 0:
                # Move the center point that we are slicing through
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                translationInterval = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [self.currentSphereWidgetCenter["coronal"][i] + translationInterval[i] for i in range(3)]
                self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])

                # Set crosshair position in coronal view
                self.setCrosshairPositionCoronalView(newPosition)
                # Set camera position in coronal view
                self.rendererCoronal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
                self.rendererCoronal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

                # Set crosshair position in axial view
                self.setCrosshairPositionAxialView(newPosition)
                # Set rotation position on green line in axial view
                # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
                # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
                # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
                
                # Set crosshair position in sagittal view
                self.setCrosshairPositionSagittalView(newPosition)

        # Sagittal view
        elif viewId == 3:
            sliceSpacing = self.resliceSagittal.GetOutput().GetSpacing()[2]
            cameraPosition = self.rendererSagittal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererSagittal.GetActiveCamera().GetFocalPoint()

            if "spinY" in event and event["spinY"] and event["spinY"] < 0:
                # Move the center point that we are slicing through
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                translationInterval = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [self.currentSphereWidgetCenter["sagittal"][i] + translationInterval[i] for i in range(3)]
                self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])

                # Set crosshair position in sagittal view
                self.setCrosshairPositionSagittalView(newPosition)
                # Set camera position in sagittal view
                self.rendererSagittal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
                self.rendererSagittal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

                # Set crosshair position in axial view
                self.setCrosshairPositionAxialView(newPosition)
                # Set rotation position on green line in axial view
                # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
                # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
                # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

                # Set crosshair position in coronal view
                self.setCrosshairPositionCoronalView(newPosition)

            elif "spinY" in event and event["spinY"] and event["spinY"] > 0:
                # Move the center point that we are slicing through
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                translationInterval = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [self.currentSphereWidgetCenter["sagittal"][i] + translationInterval[i] for i in range(3)]
                self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])

                # Set crosshair position in sagittal view
                self.setCrosshairPositionSagittalView(newPosition)
                # Set camera position in sagittal view
                self.rendererSagittal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
                self.rendererSagittal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

                # Set crosshair position in axial view
                self.setCrosshairPositionAxialView(newPosition)
                # Set rotation position on green line in axial view
                # translationInterval = [newPosition[i] - self.currentSphereWidgetCenter["axial"][i] for i in range(3)]
                # self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
                # self.currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

                # Set crosshair position in coronal view
                self.setCrosshairPositionCoronalView(newPosition)

        self.currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
        self.currentSphereWidgetCenter["coronal"] = self.sphereWidgetCoronal.GetCenter()
        self.currentSphereWidgetCenter["sagittal"] = self.sphereWidgetSagittal.GetCenter()

        self.getApplication().GetObjectIdMap().GetActiveObject("AXIAL_VIEW").Render()
        self.getApplication().GetObjectIdMap().GetActiveObject("CORONAL_VIEW").Render()
        self.getApplication().GetObjectIdMap().GetActiveObject("SAGITTAL_VIEW").Render()
        if 'End' in event["type"]:
            self.getApplication().InvokeEvent(vtkCommand.EndInteractionEvent)
