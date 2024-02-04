from textwrap import dedent

from .shelf import Shelf

class ToolkitShelf(Shelf):

    def __init__(self):
        # type: () -> None
        Shelf.__init__(self, name="Toolkit_Utils")

    def build(self):
        
        self.addButton(
            label="Print Selection",
            tooltip="Print current selection.",
            command=dedent(
                """
                from maya import cmds
                print(cmds.ls(sl=1))
                """
            )
        )

        self.addSeperator()

        self.addButton(
            label="Clear Selection",
            tooltip="Clear current selection.",
            command=dedent(
                """
                from maya import cmds
                cmds.select(cl=True)
                """
            )
        )

