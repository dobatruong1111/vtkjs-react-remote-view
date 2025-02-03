import argparse
from wslink import server
from vtk.web import wslink as vtk_wslink # type: ignore
from vtk.web import protocols as vtk_protocols # type: ignore
import vtk

from vtk_protocol import VtkCone
from endo_viewer import EndoscopyInteractorStyle
from styles import RotateInteractorStyle

class _Server(vtk_wslink.ServerProtocol):
    authKey = "wslink-secret"
    view = None

    def initialize(self):
        # Bring used components
        self.registerVtkWebProtocol(vtk_protocols.vtkWebMouseHandler())
        self.registerVtkWebProtocol(vtk_protocols.vtkWebViewPort())
        self.registerVtkWebProtocol(vtk_protocols.vtkWebPublishImageDelivery(decode=False))

        # Custom API
        self.registerVtkWebProtocol(VtkCone())

        # tell the C++ web app to use no encoding.
        # ParaViewWebPublishImageDelivery must be set to decode=False to match.
        self.getApplication().SetImageEncoding(0)

        # Update authentication key to use
        self.updateSecret(_Server.authKey)

        if not _Server.view:
            # Volume
            render_window_volume = vtk.vtkRenderWindow()
            render_window_volume.OffScreenRenderingOn()
            # Turn off warning
            render_window_volume.GlobalWarningDisplayOff()
            renderer_volume = vtk.vtkRenderer()
            render_window_volume.AddRenderer(renderer_volume)
            interactor_volume = vtk.vtkRenderWindowInteractor()
            # style = vtk.vtkInteractorStyle()
            style = RotateInteractorStyle()
            # style = vtk.vtkInteractorStyleTrackballCamera()
            interactor_volume.SetInteractorStyle(style)
            render_window_volume.SetInteractor(interactor_volume)
            self.getApplication().GetObjectIdMap().SetActiveObject("VOLUME_VIEW", render_window_volume)

            # Axial
            render_window_axial = vtk.vtkRenderWindow()
            render_window_axial.OffScreenRenderingOn()
            # renderer_axial = vtk.vtkRenderer()
            # render_window_axial.AddRenderer(renderer_axial)
            interactor_axial = vtk.vtkRenderWindowInteractor()
            pick_axial = vtk.vtkWorldPointPicker()
            interactor_axial.SetPicker(pick_axial)
            render_window_axial.SetInteractor(interactor_axial)
            self.getApplication().GetObjectIdMap().SetActiveObject("AXIAL_VIEW", render_window_axial)

            # Coronal
            render_window_coronal = vtk.vtkRenderWindow()
            render_window_coronal.OffScreenRenderingOn()
            # renderer_coronal = vtk.vtkRenderer()
            # render_window_coronal.AddRenderer(renderer_coronal)
            interactor_coronal = vtk.vtkRenderWindowInteractor()
            pick_coronal = vtk.vtkWorldPointPicker()
            interactor_coronal.SetPicker(pick_coronal)
            render_window_coronal.SetInteractor(interactor_coronal)
            self.getApplication().GetObjectIdMap().SetActiveObject("CORONAL_VIEW", render_window_coronal)

            # Sagital
            render_window_sagital = vtk.vtkRenderWindow()
            render_window_sagital.OffScreenRenderingOn()
            # renderer_sagital = vtk.vtkRenderer()
            # render_window_sagital.AddRenderer(renderer_sagital)
            interactor_sagital = vtk.vtkRenderWindowInteractor()
            pick_sagital = vtk.vtkWorldPointPicker()
            interactor_sagital.SetPicker(pick_sagital)
            render_window_sagital.SetInteractor(interactor_sagital)
            self.getApplication().GetObjectIdMap().SetActiveObject("SAGITAL_VIEW", render_window_sagital)

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Demo")

    # Add arguments
    server.add_arguments(parser)
    args = parser.parse_args()

    # Start server
    server.start_webserver(options=args, protocol=_Server, disableLogging=True)
