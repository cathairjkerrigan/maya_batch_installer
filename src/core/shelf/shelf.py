import maya.cmds as cmds
import maya.mel as mel
from typing import Any

def _null(*args):
    # type: (Any) -> None
    pass

class Shelf(object):

    def __init__(self, name='custom_shelf', icon_path=""):
        # type: (str, str) -> None
        self.name = name
        self.icon_path = icon_path

        self.label_background = (0, 0, 0, 0)
        self.label_color = (0.9, 0.9, 0.9)

        self._clean()
        cmds.setParent(self.name)
        self.build()

    def build(self):
        # type: () -> None
        pass

    def addButton(
            self, 
            label,
            tooltip,
            icon="commandButton.png",
            command=_null,
            double_command=_null,
    ):
        
        cmds.setParent(self.name)

        if icon:
            icon = self.icon_path + icon
        
        cmds.shelfButton(
            width=32,
            height=32,
            image=icon,
            label=label,
            annotation=tooltip,
            command=command,
            dcc=double_command,
            imageOverlayLabel=label,
            olb=self.label_background,
            olc=self.label_color,
            scaleIcon=True,
        )

    def addSeperator(self):
        # type: () -> None
        mel.eval("addShelfSeparator")

    def _clean(self):
        # type: () -> None
        if cmds.shelfLayout(self.name, ex=1):
            if cmds.shelfLayout(self.name, q=1, ca=1):
                for each in cmds.shelfLayout(self.name, q=1, ca=1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p="ShelfLayout")