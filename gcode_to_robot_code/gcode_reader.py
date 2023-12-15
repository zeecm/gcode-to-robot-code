"""
The code defines a class GcodeReader that reads a Gcode file, parses the movement commands, and creates an ObjectPathModel representing the path of objects in a 3D space.

The GcodeReader class has the following key components:

The constructor initializes the necessary variables.
The read_file method reads the Gcode file, parses the commands, and updates the ObjectPathModel.
The _read_filelines method reads the lines of the Gcode file and calls the _parse_command method for each line.
The _check_for_valid_gcode_file method checks if the file has a valid Gcode extension.
The _update_model method creates an ObjectPathModel instance from the parsed coordinates.
The _parse_command method parses the movement commands and extracts the X, Y, and Z coordinates.
The _identify_mesh_start method identifies the start of the mesh section in the Gcode file.
The _parse_movement_command method parses the movement command and returns a CartesianCoordinate object.
"""

from typing import Dict, List

from loguru import logger

from gcode_to_robot_code.constants import CartesianCoordinate, CartesianCoordinateAxis
from gcode_to_robot_code.model import ObjectPathModel


class GcodeReader:
    def __init__(self, slicer_layer_height: float = 0.2):
        self._model: ObjectPathModel
        self._parsed_coordinates: List[Dict[CartesianCoordinateAxis, float]] = []

        self._current_coordinate: CartesianCoordinate = CartesianCoordinate(
            0.0, 0.0, 0.0
        )
        self._slicer_layer_height = slicer_layer_height

        self._mesh_start = False

    def read_file(self, filepath: str) -> ObjectPathModel:
        self._check_for_valid_gcode_file(filepath)
        self._read_filelines(filepath)
        self._update_model()
        return self._model

    def _read_filelines(self, filepath: str) -> None:
        logger.info(f"reading gcode file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            filelines = file.readlines()
            for line in filelines:
                self._parse_command(line)
        logger.info("reading complete")

    def _check_for_valid_gcode_file(self, filepath: str) -> None:
        if not filepath.endswith(".gcode"):
            error_msg = f"invalid gcode file {filepath}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _update_model(self) -> None:
        logger.info("updating model")
        self._model = ObjectPathModel.from_coordinates(self._parsed_coordinates)
        logger.info("model update done")

    def _parse_command(self, command_line: str) -> None:
        command_components = command_line.strip().split()

        if not command_components:
            return

        self._identify_mesh_start(command_line)

        if not self._mesh_start:
            return

        if command_components[0] in ["G0", "G1"]:
            coordinate = self._parse_movement_command(command_components)
            self._current_coordinate = coordinate
            self._parsed_coordinates.append(
                {
                    CartesianCoordinateAxis.X: coordinate.x,
                    CartesianCoordinateAxis.Y: coordinate.y,
                    CartesianCoordinateAxis.Z: coordinate.z,
                }
            )

    def _identify_mesh_start(self, command_line: str) -> None:
        if self._mesh_start:
            return
        if command_line.strip().startswith(";MESH:"):
            self._mesh_start = True

    def _parse_movement_command(
        self, command_components: List[str]
    ) -> CartesianCoordinate:
        x_value = None
        y_value = None
        z_value = None

        for command in command_components:
            if command.startswith(";"):
                break
            if command.startswith("X"):
                x_value = float(command[1:])
            elif command.startswith("Y"):
                y_value = float(command[1:])
            elif command.startswith("Z"):
                z_value = float(command[1:]) - self._slicer_layer_height

        x_value = x_value if x_value is not None else self._current_coordinate.x
        y_value = y_value if y_value is not None else self._current_coordinate.y
        z_value = z_value if z_value is not None else self._current_coordinate.z

        return CartesianCoordinate(x_value, y_value, z_value)
