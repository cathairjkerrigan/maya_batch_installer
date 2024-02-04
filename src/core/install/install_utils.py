import os
from maya import cmds
from textwrap import dedent
import shutil
import logging
import sys
import webbrowser
from typing import Optional, Tuple

if sys.version_info >= (3, 5):
    from subprocess import run
else:
    from subprocess import call as run

logger = logging.getLogger(__name__)

def return_maya_version():
    # type: () -> str
    return cmds.about(version=True)

def return_maya_install():
    # type: () -> Optional[str]
    maya_folder = os.environ["MAYA_LOCATION"]
    maya_exe = os.path.join(maya_folder, "bin", "maya.exe")

    if os.path.exists(maya_exe):
        return maya_exe
    else:
        return None
    
def get_documents_folder():
    # type: () -> str
    documents_folder = os.path.dirname(os.environ["MAYA_APP_DIR"])
    return documents_folder

def create_bat_file(module_path):
    # type: (str) -> Tuple[str, str]
    maya_version = return_maya_version()
    maya_install_path = return_maya_install()
    bat_file_name = "Maya_{}.bat".format(maya_version)
    bat_file_path = os.path.join(module_path, bat_file_name)

    with open(bat_file_path, "w") as bat_file:

        bat_file.seek(0)

        bat_file.write(
            dedent(
                """
                +@echo off
                setlocal

                set MAYA_MODULE_PATH=%~dp0;%MAYA_MODULE_PATH%
                set MAYA_DISABLE_CLIC_IPM=1
                set MAYA_DISABLE_CIP=1
                set MAYA_DISABLE_CER=1 
                set MAYA_VP2_WANT_OGS_WARNINGS=1
                set MAYA_NO_WARNING_FOR_MISSING_DEFAULT_RENDERER=1
                set MAYA_SKIP_USERSETUP_CHECK=1

                rem Start Maya
                start "" "{}" -hideConsole

                endlocal
                """.format(maya_install_path)
            )
        )

        bat_file.truncate()

    return bat_file_path, bat_file_name

def create_mod_file(module_path):
    # type: (str) -> Tuple[str, str]
    maya_version = return_maya_version()
    module_name = os.path.basename(module_path)
    mod_file_name = "{}.mod".format(module_name)
    mod_file_path = os.path.join(module_path, mod_file_name)

    with open(mod_file_path, "w") as mod_file:

        mod_file.seek(0)

        mod_file.write(
            dedent(
                """
                + MAYAVERSION:{0} PLATFORM:win64 {1} 1.0 .
                PATH+:=./bin/win64;
                MAYA_PLUG_IN_PATH+:=maya/plug-ins
                MAYA_PLUG_IN_PATH+:=maya/plug-ins/{0}/win64
                icons: ./maya/icons
                presets: ./maya/presets
                scripts: ./src
                """.format(maya_version, module_name)
            )
        )

        mod_file.truncate()

    return mod_file_path, mod_file_name

def copy_folder(src, dest):
    # type: (str, str) -> str
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        
        shutil.copytree(src, dest, symlinks=True)
        logger.info("Folder '{}' successfully copied to '{}'".format(src, dest))
        return dest
    except Exception as e:
        logger.warning("Error copying folder '{}': {}".format(src, e))

def open_folder(folder_path):
    # type: (str) -> None
    os.startfile(folder_path)

def run_program(program_path):
    # type: (str) -> None
    if os.path.exists(program_path):
        run(program_path)

def return_module_name(module_path):
    return str(os.path.basename(module_path))

def path_exists(path):
    return os.path.exists(path)
    