import constants as const

from vtk_utils import TextZero

class SliceData:
    def __init__(self) -> None:
        self.actor = None
        self.text = None
        self.layer = 99
        self.number = 0
        self.orientation = "AXIAL"
        self.renderer = None
        self.canvas_renderer = None
        self.overlay_renderer = None
        self.__create_text()

    def __create_text(self) -> None:
        text = TextZero()
        text.SetSize(const.TEXT_SIZE_SMALL)
        text.SetPosition(const.TEXT_POS_LEFT_DOWN_ZERO)
        text.SetValue(self.number)
        self.text = text

    def SetNumber(self, init: int) -> None:
        self.text.SetValue("%d" % init)
        self.number = init

    def SetOrientation(self, orientation: str) -> None:
        self.orientation = orientation

    def Hide(self) -> None:
        self.overlay_renderer.RemoveActor(self.actor)
        self.renderer.RemoveActor(self.text.actor)
    
    def Show(self) -> None:
        self.renderer.AddActor(self.actor)
        self.renderer.AddActor(self.text.actor)
