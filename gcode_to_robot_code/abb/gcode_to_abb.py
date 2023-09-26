from enum import Enum
from typing import List

from loguru import logger

from gcode_to_robot_code.constants import Coordinate, ProjectionMode
from gcode_to_robot_code.gcode_reader import GcodeReader
from gcode_to_robot_code.model import ObjectModel


class MoveType(Enum):
    LINEAR = "moveL"
    PATHFINDING = "moveJ"
    CURVE = "moveC"


class ABBTranslator:
    def __init__(self, model: ObjectModel):
        self._model = model

        self._rotation = "[-1, 0, 0, 0]"
        self._conf = "[-1, 0, 1, 0]"
        self._tool = "tool0"
        self._world_object = "wobj0"

        self._robtargets = []
        self._move_commands = []

    def generate_abb_code(self) -> None:
        logger.info("generating abb code...")
        for point in range(self._model.pathlength - 1):
            point_name = f"p{point}"
            coordinate = self._model.get_point(point)
            self._write_robtarget(coordinate, point_name)
            self._write_movement(point_name)
        logger.info("generation of abb rapid code done")

    def save_abb_code(
        self,
        robtargets_filepath: str = "robtargets.txt",
        movement_filepath: str = "movements.txt",
    ) -> None:
        data_mapping = {
            robtargets_filepath: self._robtargets,
            movement_filepath: self._move_commands,
        }
        for filepath, data in data_mapping.items():
            self._write_to_file(data, filepath)

    def _write_to_file(self, data: List[str], filepath: str) -> None:
        with open(filepath, "w") as file:
            for line in data:
                file.writelines(line)

    def _write_robtarget(self, coordinate: Coordinate, point_name: str) -> None:
        robtarget = (
            f":= [[{str(coordinate.x)},{str(coordinate.y)},{str(coordinate.z)}], {self._rotation},{self._conf}, [ 9E+9,9E+9, 9E9, 9E9, 9E9, 9E9]];"
            + "\n"
        )
        robtarget_line = f"CONST robtarget {point_name}{robtarget}"
        self._robtargets.append(robtarget_line)

    def _write_movement(
        self, point_name: str, move_type: MoveType = MoveType.LINEAR
    ) -> None:
        move_command = f"{move_type.value} {point_name},v100,fine,{self._tool}\WObj:={self._world_object};\n"
        self._move_commands.append(move_command)


if __name__ == "__main__":
    reader = GcodeReader()
    gcode_object = reader.read_file(
        r"gcode_to_robot_code\gcode_files\BB1_cylinder.gcode"
    )
    abb_translator = ABBTranslator(gcode_object)
    # abb_translator.generate_abb_code()
    # abb_translator.save_abb_code()
    gcode_object.plot_path(projection=ProjectionMode.THREE_DIMENSIONAL)
