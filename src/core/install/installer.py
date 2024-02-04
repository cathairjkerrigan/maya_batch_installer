from .install_utils import create_bat_file, create_mod_file, copy_folder, get_documents_folder, run_program, open_folder
import os
from maya import cmds
from typing import Optional

def install_module(module_path, copy_to_folder=True, copy_path=None, restart_maya=True, should_open_folder=True):
    # type: (str, Optional[bool], Optional[str], Optional[bool], Optional[bool]) -> None
    # create the batch file
    _, batch_name = create_bat_file(module_path)

    # create the mod file
    create_mod_file(module_path)

    if copy_to_folder is True:
        # get the documents path from maya's MAYA_APP_DIR
        if copy_path is None:
            copy_path = get_documents_folder()

        # construct new path to copy module to
        module_name = os.path.basename(module_path)
        new_module_path = os.path.join(copy_path, module_name)

        # copy module to docs folder, removing previous folder if it exists
        new_module = copy_folder(module_path, new_module_path)

    if copy_to_folder is True and should_open_folder is True:
        # finally open the folder where the new files and batch are located
        open_folder(new_module)

    if restart_maya is True:
        # close maya
        cmds.quit()

        # relaunch maya with the new batch file
        new_batch_location = os.path.join(new_module_path, batch_name)

        run_program(new_batch_location)