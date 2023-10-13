import os
from tempfile import TemporaryDirectory

import pytest

from gcode_to_robot_code.abb.abb_generator import ABBModuleGenerator
from gcode_to_robot_code.gcode_reader import GcodeReader


@pytest.mark.parametrize(
    "gcode_filepath, expected_module_filepath, module_name, procedure_name",
    [
        (
            "gcode_to_robot_code/gcode_files/mencast_logo.gcode",
            "tests/integration_tests/sample_generated_modules/mencast_logo.mod.test",
            "Logo",
            "DrawLogo",
        ),
        (
            "gcode_to_robot_code/gcode_files/EllipseV3.gcode",
            "tests/integration_tests/sample_generated_modules/ellipse.mod.test",
            "Ellipse",
            "DrawEllipse",
        ),
        (
            "gcode_to_robot_code/gcode_files/cylinder.gcode",
            "tests/integration_tests/sample_generated_modules/cylinder.mod.test",
            "Cylinder",
            "DrawCylinder",
        ),
    ],
)
def test_abb_module_generator_from_gcode(
    gcode_filepath: str,
    expected_module_filepath: str,
    module_name: str,
    procedure_name: str,
):
    reader = GcodeReader()
    model = reader.read_file(gcode_filepath)
    abb_generator = ABBModuleGenerator(
        model=model, module_name=module_name, procedure_name=procedure_name
    )
    with TemporaryDirectory() as tmpdir:
        save_path = os.path.join(tmpdir, "test_mod.mod")
        abb_generator.generate_robtargets_and_move_commands()
        abb_generator.save_as_module(save_path)
        assert _compare_files(save_path, expected_module_filepath)


def _compare_files(filepath1: str, filepath2: str) -> bool:
    with open(filepath1, "r", encoding="utf-8") as saved_file:
        with open(filepath2, "r", encoding="utf-8") as expected_file:
            return saved_file.read() == expected_file.read()
