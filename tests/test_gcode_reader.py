import os

import pytest

from gcode_to_robot_code.gcode_reader import GcodeReader
from gcode_to_robot_code.model import ObjectPathModel


class TestGcodeReader:
    def setup_method(self):
        self.reader = GcodeReader()

    @pytest.mark.parametrize(
        "gcode_filepath",
        [
            (os.path.join("gcode_to_robot_code", "gcode_files", "cylinder.gcode")),
            (os.path.join("gcode_to_robot_code", "gcode_files", "cylinder_v2.gcode")),
            (os.path.join("gcode_to_robot_code", "gcode_files", "mencast_logo.gcode")),
        ],
    )
    def test_read_file(self, gcode_filepath: str):
        model = self.reader.read_file(gcode_filepath)
        assert isinstance(model, ObjectPathModel)
