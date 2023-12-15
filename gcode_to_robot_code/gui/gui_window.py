from loguru import logger
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from gcode_to_robot_code.abb.abb_generator import ABBModuleGenerator
from gcode_to_robot_code.gcode_reader import GcodeReader
from gcode_to_robot_code.gui.gui_classes import DialogFileType, PandasModel
from gcode_to_robot_code.gui.pyside_files.generated.app_window import (
    Ui_GcodeToRobotCodeWindow,
)


class GcodeToRobotCodeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GcodeToRobotCodeWindow()
        self.ui.setupUi(self)

        self._setup_buttons()

        self._reader = GcodeReader()
        self._abb_generator = None
        self._model = None

    def _setup_buttons(self) -> None:
        self.ui.read_gcode_button.clicked.connect(self._read_gcode_button_clicked)
        self.ui.optimize_straight_line_button.clicked.connect(
            self._optimize_straight_lines
        )
        self.ui.generate_abb_code_button.clicked.connect(
            self._generate_abb_rapid_code_button_clicked
        )
        self.ui.select_gcode_file_button.clicked.connect(self._select_gcode_file)
        self.ui.save_module_button.clicked.connect(self._save_module)

    def _read_gcode_button_clicked(self) -> None:
        filepath = self.ui.gcode_filepath_lineedit.text()
        self._model = self._reader.read_file(filepath)
        self._update_toolpath_data_table()

    def _update_toolpath_data_table(self) -> None:
        if self._model is None:
            logger.error("No GCODE file is loaded, please check")
            return
        logger.info("updating toolpath table")
        model = PandasModel(self._model.toolpath_data, show_index=True)
        self.ui.toolpath_data_table.setModel(model)
        self.ui.toolpath_data_table.resizeColumnsToContents()

    def _optimize_straight_lines(self) -> None:
        if self._model is not None:
            self._model.optimize_straight_lines()
            self._update_toolpath_data_table()

    def _select_gcode_file(self) -> None:
        gcode_filetype = DialogFileType("Gcode Files", extensions=["gcode"])
        gcode_filepath = self._open_filedialog(
            "Select Gcode File", filetypes=gcode_filetype
        )
        if gcode_filepath is not None:
            self.ui.gcode_filepath_lineedit.setText(gcode_filepath)

    def _open_filedialog(
        self,
        title: str,
        filetypes: DialogFileType,
        directory="",
        enable_all_files: bool = False,
    ) -> str:
        filter_str = filetypes.pyside6_filter_str
        if enable_all_files:
            filter_str += ";;All Files (*)"
        filepath, _ = QFileDialog.getOpenFileName(self, title, directory, filter_str)
        return filepath

    def _generate_abb_rapid_code_button_clicked(self) -> None:
        self._generate_abb_targets_and_commands()
        self._display_robtargets_and_move_commands()
        self._display_module_preview()

    def _generate_abb_targets_and_commands(self) -> None:
        if self._model is None:
            logger.error("No GCODE file is loaded, please check")
            return
        module_name = self.ui.module_name_lineedit.text()
        procedure_name = self.ui.procedure_name_lineedit.text()
        self._abb_generator = ABBModuleGenerator(
            model=self._model, module_name=module_name, procedure_name=procedure_name
        )
        self._abb_generator.generate_robtargets_and_move_commands()

    def _display_robtargets_and_move_commands(self) -> None:
        if self._abb_generator is None:
            logger.error("cannot call this method without initializing abb generator")
            return
        robtargets_text = "\n".join(self._abb_generator.robtargets)
        move_commands_text = "\n".join(self._abb_generator.move_commands)
        logger.info("updating robtargets and move commands display...")
        self.ui.robtargets_text.setText(robtargets_text)
        self.ui.move_commands_text.setText(move_commands_text)
        logger.info("robtargets and move commands display updated")

    def _display_module_preview(self) -> None:
        if self._abb_generator is None:
            logger.error("cannot call this method without initializing abb generator")
            return
        logger.info("updating module preview display...")
        module_text_data = self._abb_generator.generate_module_text()
        text = "\n".join(module_text_data)
        self.ui.module_preview_text.setText(text)
        logger.info("module preview display updated")

    def _save_module(self) -> None:
        filename = self.ui.save_filepath_lineedit.text()
        if not filename.lower().endswith(".mod"):
            filename += ".mod"
        dialog = QMessageBox(self)
        if self._abb_generator is None:
            dialog.setWindowTitle("ABB Code Not Generated")
            dialog.setText("Unable to save as ABB Code has not been generated")
        else:
            rapid_mod_file_filter_str = "RAPID MOD Files (*.mod)"
            filepath, _ = QFileDialog().getSaveFileName(
                self,
                "Save Module",
                dir=f"./{filename}",
                filter=rapid_mod_file_filter_str,
            )
            if filepath is not None:
                result, err_str = self._abb_generator.save_as_module(filepath)
                if result:
                    success_msg = f"Saved module to {filepath}"
                    dialog.setWindowTitle("Saved!")
                    dialog.setText(success_msg)
                    logger.info(success_msg)
                else:
                    dialog.setWindowTitle("Error Saving Module")
                    dialog.setText(f"Failed to save with error: {err_str}")
                    logger.error(err_str)
        dialog.exec_()
