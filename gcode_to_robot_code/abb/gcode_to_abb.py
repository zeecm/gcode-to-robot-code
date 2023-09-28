from __future__ import annotations

from enum import Enum
from typing import List, NamedTuple, Optional, Union

from loguru import logger

from gcode_to_robot_code.abb.data_types import LoadData, Pose, ToolData, ToolInfo
from gcode_to_robot_code.constants import CartesianCoordinate, ProjectionMode
from gcode_to_robot_code.gcode_reader import GcodeReader
from gcode_to_robot_code.model import ObjectToolPath


class MoveType(Enum):
    LINEAR = "moveL"
    PATHFINDING = "moveJ"
    CURVE = "moveC"


_INDENTATION = "    "


class CodeBlock(NamedTuple):
    start_line: str
    end_line: str
    code: Optional[List[Union[CodeBlock, List[str]]]]

    def generate_text_list(self) -> List[str]:
        code = self._generate_nested_code()
        return [
            self.start_line,
            *code,
            self.end_line,
        ]

    def _generate_nested_code(self) -> List[str]:
        if self.code is None:
            return []
        code = []
        for nested_code in self.code:
            if isinstance(nested_code, CodeBlock):
                nested_code = nested_code.generate_text_list()
            code.extend([_INDENTATION + code_line for code_line in nested_code])
            code.append("\n")
        return code


_DEFAULT_TOOL_DATA = ToolData(
    robhold=True,
    tframe=Pose(
        trans=[0, 0, 0],
        rot=[0, 0, 1, 0],
    ),
    tload=LoadData(
        mass=1,
        cog=[
            0,
            0,
            1,
        ],
        aom=[1, 0, 0, 0],
        ix=0,
        iy=0,
        iz=0,
    ),
)
_DEFAULT_TOOL_NAME = "tool1"

DEFAULT_TOOL = ToolInfo(name=_DEFAULT_TOOL_NAME, data=_DEFAULT_TOOL_DATA)

DEFAULT_OFFSET = CartesianCoordinate(x=1000.0, y=-50.0, z=500.0)


class ABBModuleGenerator:
    def __init__(
        self,
        model: ObjectToolPath,
        module_name: str = "MahModule",
        procedure_name: str = "TestProc",
        tool: ToolInfo = DEFAULT_TOOL,
        default_movetype: MoveType = MoveType.PATHFINDING,
        target_offsets: CartesianCoordinate = DEFAULT_OFFSET,
    ):
        self._model = model

        self._module_name = module_name
        self._procedure_name = procedure_name

        self._target_rotation = "[-1, 0, 0, 0]"
        self._target_conf = "[-1, 0, 1, 0]"
        self._tool = tool
        self._world_object = "wobj0"
        self._target_offsets = target_offsets

        self._default_movetype = default_movetype

        self._robtargets: List[str] = []
        self._move_commands: List[str] = []

    def generate_robtargets_and_movements(self) -> None:
        logger.info("generating abb code...")
        for point in range(self._model.pathlength - 1):
            point_name = f"p{point}"
            coordinate = self._model.get_point(point)
            self._write_robtarget(coordinate, point_name)
            self._write_movement(point_name)
        logger.info("generation of abb rapid code done")

    def save_robtargets_and_movements_to_text(
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
        with open(filepath, "w", encoding="utf-8") as file:
            for line in data:
                file.writelines(line)

    def _write_robtarget(
        self, coordinate: CartesianCoordinate, point_name: str
    ) -> None:
        adjusted_x = coordinate.x + self._target_offsets.x
        adjusted_y = coordinate.y + self._target_offsets.y
        adjusted_z = coordinate.z + self._target_offsets.z

        robtarget = (
            f":= [[{str(adjusted_x)},{str(adjusted_y)},{str(adjusted_z)}], {self._target_rotation},{self._target_conf}, [ 9E+9,9E+9, 9E9, 9E9, 9E9, 9E9]];"
            + "\n"
        )
        robtarget_line = f"CONST robtarget {point_name}{robtarget}"
        self._robtargets.append(robtarget_line)

    def _write_movement(
        self, point_name: str, movetype: Optional[MoveType] = None
    ) -> None:
        movetype = movetype or MoveType.PATHFINDING
        move_command = f"{movetype.value} {point_name},v100,fine,{self._tool.name}\WObj:={self._world_object};\n"
        self._move_commands.append(move_command)

    @property
    def tooldata_line(self) -> str:
        tool_data = self._tool.data
        rob_hold = tool_data.robhold
        tframe = tool_data.tframe
        tload = tool_data.tload

        tooldata_str = f"[{rob_hold},[{tframe.trans},{tframe.rot}],[{tload.mass},{tload.cog},{tload.aom},{tload.ix},{tload.iy},{tload.iz}]]"

        return f"PERS tooldata {self._tool.name}:={tooldata_str};\n"

    def save_module(self, module_filepath: Optional[str] = None) -> None:
        module_filepath = module_filepath or f"{self._module_name}.mod"
        module = self._generate_abb_module()
        module_text_data = module.generate_text_list()
        self._write_to_file(module_text_data, module_filepath)

    def _generate_abb_module(self) -> CodeBlock:
        module_declaration = f"MODULE {self._module_name}\n"
        module_end = "ENDMODULE\n"
        tool = self.tooldata_line
        procedure = self._generate_procedure_codeblock()
        code = [[tool], self._robtargets, procedure]
        return CodeBlock(start_line=module_declaration, end_line=module_end, code=code)

    def _generate_procedure_codeblock(self) -> CodeBlock:
        procedure_declaration = f"PROC {self._procedure_name}()\n"
        procedure_close = "ENDPROC\n"
        return CodeBlock(
            start_line=procedure_declaration,
            end_line=procedure_close,
            code=[self._move_commands],
        )


if __name__ == "__main__":
    reader = GcodeReader()
    gcode_object = reader.read_file(
        r"gcode_to_robot_code\gcode_files\BB1_cylinder v2.gcode"
    )
    gcode_object.optimize_straight_line()

    # gcode_object.plot_path(projection=ProjectionMode.THREE_DIMENSIONAL)
    generator = ABBModuleGenerator(model=gcode_object)
    generator.generate_robtargets_and_movements()
    generator.save_module()
