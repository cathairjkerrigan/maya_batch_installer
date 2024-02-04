from PySide2 import QtWidgets, QtGui
import logging
from typing import Optional
from textwrap import dedent
from src.core.install.install_utils import return_module_name, get_documents_folder, path_exists
from src.core.install.installer import install_module
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

logger = logging.getLogger(__name__)

class InstallerUI(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    _instance = None

    @classmethod
    def open(cls, module_path):
        if cls._instance is None:
            cls._instance = cls(module_path)

        cls._instance.show(dockable=True)

    def __init__(self, module_path):
        # type: (str) -> None

        super(InstallerUI, self).__init__()

        self.resize(500, 500)
        self.module_path = module_path
        self.module_name = return_module_name(self.module_path)
        
        self.custom_directory = self.module_name

        self.setWindowTitle("{0} Installer".format(self.module_name))

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self.should_reload_maya = True
        self.should_copy_folder = True
        self.copy_destination = get_documents_folder()
        self.should_open_folder = True

        self.installer_textedit = QtWidgets.QTextEdit()
        self.installer_textedit.setText(
            dedent(
                """
                --------------------
                {0} Installer
                --------------------

                Installs {0} module and creates a maya batch file to run Maya with {0}. 
                Creates a custom menu and shelf on launch of the batch file.
                Includes reload functionality to reload {0} module without closing Maya.

                --------------------
                Install Instructions
                --------------------

                Default installation will reload Maya, starting it with the generated batch
                file and copy the module to your documents folder.

                Custom installation allows you to choose whether or not to reload Maya and
                copy the module to the specified folder (by default this is your documents folder).

                --------------------
                Usage Instructions
                --------------------

                To use the {0} module with Maya, run maya with the generated batch file.
                This will automatically load the module, custom menu and shelf on launch.
                """.format(self.module_name)
            )
        )
        
        self.installer_textedit.setReadOnly(True)
    
        self._layout.addWidget(self.installer_textedit)

        self._installation_type_layout = QtWidgets.QHBoxLayout()

        self.default_installation_radiobutton = QtWidgets.QRadioButton("Default Installation")
        self.default_installation_radiobutton.setChecked(True)
        self.custom_installation_radiobutton = QtWidgets.QRadioButton("Custom Installation")

        self.default_installation_radiobutton.toggled.connect(self.check_installation_type)
        self.custom_installation_radiobutton.toggled.connect(self.check_installation_type)

        self._installation_type_layout.addWidget(self.default_installation_radiobutton)
        self._installation_type_layout.addWidget(self.custom_installation_radiobutton)

        self._custom_install_layout = QtWidgets.QVBoxLayout()

        self._custom_checks_layout = QtWidgets.QHBoxLayout()

        self.restart_maya_checkbox = QtWidgets.QCheckBox("Reload Maya")
        self.restart_maya_checkbox.setChecked(True)

        self.copy_to_folder_checkbox = QtWidgets.QCheckBox("Copy To Folder")
        self.copy_to_folder_checkbox.setChecked(True)

        self.copy_to_folder_checkbox.toggled.connect(self.toggle_file_path)

        self._custom_checks_layout.addWidget(self.restart_maya_checkbox)
        self._custom_checks_layout.addWidget(self.copy_to_folder_checkbox)
        self._custom_checks_layout.addStretch()

        self._custom_path_layout = QtWidgets.QGridLayout()

        self.custom_path_label = QtWidgets.QLabel("Copy Path: ")

        self.custom_path_lineedit = QtWidgets.QLineEdit()
        self.custom_path_lineedit.setText(self.copy_destination)
        self.custom_path_lineedit.setReadOnly(True)
        self.custom_path_button = QtWidgets.QPushButton()
        self.custom_path_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.open_folder_checkbox = QtWidgets.QCheckBox("Open Folder")
        self.open_folder_checkbox.setChecked(True)

        self.custom_path_button.clicked.connect(self.open_dir)

        self._custom_path_layout.addWidget(self.custom_path_label, 0, 0)
        self._custom_path_layout.addWidget(self.custom_path_lineedit, 0, 1)
        self._custom_path_layout.addWidget(self.custom_path_button, 0, 2)
        self._custom_path_layout.addWidget(self.open_folder_checkbox, 1, 0)

        self._custom_install_layout.addLayout(self._custom_checks_layout)
        self._custom_install_layout.addLayout(self._custom_path_layout)

        self._install_layout = QtWidgets.QHBoxLayout()

        self.run_install_pushbutton = QtWidgets.QPushButton("Run Install")
        self.close_pusbutton = QtWidgets.QPushButton("Close")

        self._install_layout.addWidget(self.run_install_pushbutton)
        self._install_layout.addWidget(self.close_pusbutton)

        self.run_install_pushbutton.clicked.connect(self.run_install)
        self.close_pusbutton.clicked.connect(self.close)

        self._layout.addLayout(self._installation_type_layout)
        self._layout.addLayout(self._custom_install_layout)
        self._layout.addLayout(self._install_layout)

        self.check_installation_type()

    def check_installation_type(self):
        if self.default_installation_radiobutton.isChecked():
            index = self._custom_install_layout.count()
            for i in reversed(range(index)):
                layout = self._custom_install_layout.itemAt(i)
                for i in reversed(range(layout.count())):
                    widget = layout.itemAt(i).widget()
                    if widget is None:
                        continue
                    widget.setVisible(False)
                    widget.updateGeometry()
                    widget.update()
        else:
            index = self._custom_install_layout.count()
            for i in reversed(range(index)):
                layout = self._custom_install_layout.itemAt(i)
                for i in reversed(range(layout.count())):
                    widget = layout.itemAt(i).widget()
                    if widget is None:
                        continue
                    widget.setVisible(True)
                    widget.updateGeometry()
                    widget.update()
                    
            self.toggle_file_path()

    def toggle_file_path(self):
        if not self.copy_to_folder_checkbox.isChecked():
            for i in reversed(range(self._custom_path_layout.count())):
                widget = self._custom_path_layout.itemAt(i).widget()
                if widget is None:
                    continue
                widget.setVisible(False)
                widget.updateGeometry()
                widget.update()
        elif self.copy_to_folder_checkbox.isChecked():
            for i in reversed(range(self._custom_path_layout.count())):
                widget = self._custom_path_layout.itemAt(i).widget()
                if widget is None:
                    continue
                widget.setVisible(True)
                widget.updateGeometry()
                widget.update()

    def open_dir(self):
        previous_path = self.custom_path_lineedit.text()
        new_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", previous_path)
        if new_directory == "":
            self.custom_path_lineedit.setText(previous_path)
            self.custom_directory = previous_path
        else:
            self.custom_path_lineedit.setText(new_directory)
            self.custom_directory = new_directory

    def run_install(self):
        if self.default_installation_radiobutton.isChecked():
            install_module(self.module_path)
            return
        
        install_module(
            self.module_path, 
            copy_to_folder=self.copy_to_folder_checkbox.isChecked(),
            copy_path=self.custom_path_lineedit.text(),
            restart_maya=self.restart_maya_checkbox.isChecked(),
            should_open_folder=self.open_folder_checkbox.isChecked()
        )