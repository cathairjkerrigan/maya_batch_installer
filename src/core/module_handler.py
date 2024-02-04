import sys
from typing import List
from logging import getLogger

DEBUG = False

logger = getLogger(__name__)

def reload_module(module_name, include_submodules=False):
    # type: (str, bool) -> None
    '''
    Function to reload modules to allow for a clean reset of a repository.

    Allows for reloading repository within Maya without restarting to test changes.

    Args:
        module_name: str
            - The module name you wish to reload, eg "repos".
        
        include_submodules: bool
            - Whether to check for submodules within the initial module and delete them as well.
    '''
    message = "Reloading {}".format(module_name)
    if include_submodules:
        message += " and its submodules"
    message += "."

    logger.info(message)

    unload_modules = []  # type: List[str]

    for module in sys.modules.copy():
        should_delete = False
        if include_submodules:
            if module_name in module:
                should_delete = True
        else:
            if module == module_name:
                should_delete = True

        if should_delete:
            unload_modules.append(module)

    for module in unload_modules:
        if DEBUG: logger.info(module)
        del sys.modules[module]
        if DEBUG: logger.info("deleted module: {}".format(module))
