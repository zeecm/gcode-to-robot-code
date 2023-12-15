import sys

from PySide6.QtWidgets import QApplication

from gcode_to_robot_code.gui.gui_window import GcodeToRobotCodeUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gcode_to_robot_code_ui = GcodeToRobotCodeUI()
    gcode_to_robot_code_ui.show()
    sys.exit(app.exec())
