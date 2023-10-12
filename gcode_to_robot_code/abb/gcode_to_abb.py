from __future__ import annotations

from enum import Enum
from typing import List, Literal, NamedTuple, Optional, Union

from loguru import logger

from gcode_to_robot_code.abb.data_types import (
    ConfData,
    LoadData,
    Pose,
    PredefinedSpeed,
    RobTarget,
    ToolData,
    ToolInfo,
)
from gcode_to_robot_code.constants import CartesianCoordinate, ProjectionMode
from gcode_to_robot_code.gcode_reader import GcodeReader
from gcode_to_robot_code.model import ObjectPathModel


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

_DEFAULT_TOOL = ToolInfo(name=_DEFAULT_TOOL_NAME, data=_DEFAULT_TOOL_DATA)

_DEFAULT_OFFSET = CartesianCoordinate(x=1000.0, y=-50.0, z=430.0)

_DEFAULT_ROTATION = [-1.0, 0.0, 0.0, 0.0]

_DEFAULT_CONF = ConfData(-1.0, 0.0, 1.0, 0.0)

_DEFAULT_EXTAX = "[9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]"

_HOME_COORDINATE = CartesianCoordinate(x=650.0, y=0.0, z=1000.0)

_HOME_ROBTARGET = RobTarget(
    trans=_HOME_COORDINATE,
    rot=_DEFAULT_ROTATION,
    robconf=_DEFAULT_CONF,
    extax=_DEFAULT_EXTAX,
)


class ABBModuleGenerator:
    def __init__(
        self,
        model: ObjectPathModel,
        module_name: str = "MahModule",
        procedure_name: str = "TestProc",
        tool: ToolInfo = _DEFAULT_TOOL,
        target_offsets: CartesianCoordinate = _DEFAULT_OFFSET,
        home: RobTarget = _HOME_ROBTARGET,
    ):
        self._model = model

        self._module_name = module_name
        self._procedure_name = procedure_name

        self._target_rotation = _DEFAULT_ROTATION
        self._target_conf = _DEFAULT_CONF
        self._target_extax = _DEFAULT_EXTAX

        self._tool = tool
        self._world_object = "wobj0"
        self._target_offsets = target_offsets
        self._home = home
        self._home_point_name = "zcHome"

        self._current_z_plane = 0.0
        self._default_movetype = MoveType.PATHFINDING

        self._robtargets: List[str] = []
        self._move_commands: List[str] = []
        self._write_robtarget(self._home, point_name=self._home_point_name)

    def _convert_movetype_to_custom_enum(
        self, move_type: Union[Literal["linear", "pathfinding", "curve"], MoveType]
    ) -> MoveType:
        if not isinstance(move_type, MoveType):
            return MoveType[move_type.upper()]
        return move_type

    def generate_robtargets_and_movements(self) -> None:
        logger.info("generating abb code...")
        self._write_move_to_home()
        for point in range(self._model.pathlength):
            point_name = f"p_{self._procedure_name}_{point}"
            coordinate = self._model.get_point(point)

            speed = self.get_speed(point, self._model.pathlength)
            movetype = self._update_zplane_and_get_movetype(coordinate)

            self._write_robtarget_from_coordinates(coordinate, point_name)
            self._write_movement(point_name, speed=speed, movetype=movetype)
        self._write_move_to_home()
        logger.info("generation of abb rapid code done")

    def get_speed(self, point_num: int, pathlength: int) -> str:
        if point_num in [0, pathlength - 1]:
            return PredefinedSpeed.V100.value
        return PredefinedSpeed.V5.value

    def _write_move_to_home(self) -> None:
        self._write_movement(
            self._home_point_name,
            movetype=MoveType.PATHFINDING,
            speed=PredefinedSpeed.V1000.value,
        )

    def _update_zplane_and_get_movetype(
        self, coordinate: CartesianCoordinate
    ) -> MoveType:
        if coordinate.z != self._current_z_plane:
            self._current_z_plane = coordinate.z
            return MoveType.PATHFINDING
        return MoveType.LINEAR

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

    def _generate_robtarget_from_coordinate(
        self,
        coordinate: CartesianCoordinate,
        offset: Optional[CartesianCoordinate] = None,
    ) -> RobTarget:
        offset = offset or self._target_offsets
        adjusted_coordinate = coordinate.offset_by_coordinate(self._target_offsets)

        return RobTarget(
            trans=adjusted_coordinate,
            rot=self._target_rotation,
            robconf=self._target_conf,
            extax=self._target_extax,
        )

    def _write_robtarget_from_coordinates(
        self,
        coordinate: CartesianCoordinate,
        point_name: str,
        offset: Optional[CartesianCoordinate] = None,
    ) -> None:
        robtarget = self._generate_robtarget_from_coordinate(coordinate, offset)
        self._write_robtarget(robtarget, point_name)

    def _write_robtarget(self, robtarget: RobTarget, point_name: str) -> None:
        robtarget_line = f"CONST robtarget {point_name} := {robtarget.to_string()};\n"
        self._robtargets.append(robtarget_line)

    def _write_movement(
        self,
        point_name: str,
        movetype: Optional[MoveType] = None,
        speed: str = PredefinedSpeed.V100.value,
    ) -> None:
        movetype = movetype or self._default_movetype
        move_command = f"{movetype.value} {point_name},{speed},fine,{self._tool.name}\WObj:={self._world_object};\n"
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
