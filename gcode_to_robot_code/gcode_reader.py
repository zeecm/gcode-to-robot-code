from typing import Dict, List

from loguru import logger

from gcode_to_robot_code.constants import CartesianCoordinate, CartesianCoordinateAxis
from gcode_to_robot_code.model import ObjectToolPath


class GcodeReader:
    def __init__(self):
        self._model: ObjectToolPath
        self._parsed_coordinates: List[Dict[CartesianCoordinateAxis, float]] = []

        self._current_coordinate: CartesianCoordinate = CartesianCoordinate(
            0.0, 0.0, 0.0
        )

    def read_file(self, filepath: str) -> ObjectToolPath:
        self._check_for_valid_gcode_file(filepath)
        self._read_filelines(filepath)
        self._update_model()
        return self._model

    def _read_filelines(self, filepath: str) -> None:
        logger.info(f"reading gcode file: {filepath}")
        with open(filepath, "r") as file:
            filelines = file.readlines()
            for line in filelines:
                self.parse_command(line)
        logger.info("reading complete")

    def _check_for_valid_gcode_file(self, filepath: str) -> None:
        if not filepath.endswith(".gcode"):
            error_msg = f"invalid gcode file {filepath}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _update_model(self) -> None:
        logger.info("updating model")
        self._model = ObjectToolPath.from_coordinates(self._parsed_coordinates)
        logger.info("model update done")

    def parse_command(self, command_line: str) -> None:
        command_components = command_line.strip().split()
        if not command_components:
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

    def _parse_movement_command(
        self, command_components: List[str]
    ) -> CartesianCoordinate:
        x = None
        y = None
        z = None

        for command in command_components:
            if command.startswith(";"):
                break
            if command.startswith("X"):
                x = float(command[1:])
            elif command.startswith("Y"):
                y = float(command[1:])
            elif command.startswith("Z"):
                z = float(command[1:])

        x = x or self._current_coordinate.x
        y = y or self._current_coordinate.y
        z = z or self._current_coordinate.z

        return CartesianCoordinate(x, y, z)
