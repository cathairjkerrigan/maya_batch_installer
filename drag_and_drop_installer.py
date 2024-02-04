import os
import logging
from maya import cmds
from textwrap import dedent
from src.core.install.ui.installer_ui import InstallerUI

logger = logging.getLogger(__name__)

def onMayaDroppedPythonFile(*args):

    mod_directory = os.path.dirname(__file__)
    InstallerUI.open(mod_directory)
