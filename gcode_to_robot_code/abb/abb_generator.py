"""
"""


from __future__ import annotations

from typing import List, NamedTuple, Optional, Tuple, Union

from loguru import logger

from gcode_to_robot_code.abb.abb_data_types import (
    MoveType,
    PredefinedSpeed,
    RobTarget,
    ToolInfo,
)
from gcode_to_robot_code.abb.abb_defaults import (
    _DEFAULT_CONF,
    _DEFAULT_EXTAX,
    _DEFAULT_OFFSET,
    _DEFAULT_ROTATION,
    _DEFAULT_TOOL,
    _HOME_ROBTARGET,
)
from gcode_to_robot_code.constants import CartesianCoordinate
from gcode_to_robot_code.model import ObjectPathModel

_INDENTATION = "    "


class CodeBlock(NamedTuple):
    """
    This piece of code defines a class called CodeBlock that represents a block of code. It has attributes for the start line, end line, and the code within the block. The class provides a method generate_text_list() that returns a list of strings representing the code block.

    The CodeBlock class has the following implementation:

    It is defined as a named tuple with three attributes: start_line, end_line, and code.
    The generate_text_list() method is defined to generate a list of strings representing the code block.
    The _generate_nested_code() method is a helper method that recursively generates the code for nested code blocks.

    """

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


class ABBModuleGenerator:
    """
    This code defines a class ABBModuleGenerator that generates ABB robot module code. The module code consists of robtargets (robot targets) and move commands. The class provides methods to generate the robtargets and move commands based on a given model, and to save them as a module file or as separate text files.

    The ABBModuleGenerator class has the following key components:

    Constructor: Initializes the class with the given model, module name, procedure name, tool information, target offsets, and home position.
    generate_robtargets_and_move_commands method: Generates the robtargets and move commands based on the model.
    Helper methods: _generate_move_to_home_command, _generate_robtargets_and_move_commands_for_model, get_speed, _update_zplane_and_get_movetype, _add_robtarget_from_coordinate, _robtarget_from_coordinate, _add_robtarget, _add_move_command: These methods are used by generate_robtargets_and_move_commands to generate the robtargets and move commands.
    save_as_module method: Saves the generated module code as a module file.
    _generate_module_codeblock method: Generates the code block for the module.
    _generate_tooldata_line method: Generates the tool data line for the module.
    _generate_procedure_codeblock method: Generates the code block for the procedure.
    save_robtargets_and_movements_to_text method: Saves the generated robtargets and move commands as separate text files.
    _write_to_file method: Writes the data to a file.

    """

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
        self._add_robtarget(self._home, point_name=self._home_point_name)

    @property
    def move_commands(self):
        return self._move_commands.copy()

    @property
    def robtargets(self):
        return self._robtargets.copy()

    def generate_robtargets_and_move_commands(self) -> None:
        logger.info("generating robtargets and move commands...")
        self._generate_move_to_home_command()
        self._generate_robtargets_and_move_commands_for_model()
        self._generate_move_to_home_command()
        logger.info("generation done")

    def _generate_move_to_home_command(self) -> None:
        self._add_move_command(
            self._home_point_name,
            movetype=MoveType.PATHFINDING,
            speed=PredefinedSpeed.V1000.value,
        )

    def _generate_robtargets_and_move_commands_for_model(self) -> None:
        for point in range(self._model.pathlength):
            point_name = f"p_{self._procedure_name}_{point}"
            coordinate = self._model.get_point(point)

            speed = self.get_speed(point, self._model.pathlength)
            movetype = self._update_zplane_and_get_movetype(coordinate)

            self._add_robtarget_from_coordinate(coordinate, point_name)
            self._add_move_command(point_name, speed=speed, movetype=movetype)

    def get_speed(self, point_num: int, pathlength: int) -> str:
        if point_num in [0, pathlength - 1]:
            return PredefinedSpeed.V100.value
        return PredefinedSpeed.V5.value

    def _update_zplane_and_get_movetype(
        self, coordinate: CartesianCoordinate
    ) -> MoveType:
        if coordinate.z != self._current_z_plane:
            self._current_z_plane = coordinate.z
            return MoveType.PATHFINDING
        return MoveType.LINEAR

    def _add_robtarget_from_coordinate(
        self,
        coordinate: CartesianCoordinate,
        point_name: str,
        offset: Optional[CartesianCoordinate] = None,
    ) -> None:
        robtarget = self._robtarget_from_coordinate(coordinate, offset)
        self._add_robtarget(robtarget, point_name)

    def _robtarget_from_coordinate(
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

    def _add_robtarget(self, robtarget: RobTarget, point_name: str) -> None:
        robtarget_line = f"CONST robtarget {point_name} := {robtarget.to_string()};\n"
        self._robtargets.append(robtarget_line)

    def _add_move_command(
        self,
        point_name: str,
        movetype: Optional[MoveType] = None,
        speed: str = PredefinedSpeed.V100.value,
    ) -> None:
        movetype = movetype or self._default_movetype
        move_command = f"{movetype.value} {point_name},{speed},fine,{self._tool.name}\WObj:={self._world_object};\n"
        self._move_commands.append(move_command)

    def save_as_module(self, module_filepath: Optional[str] = None) -> Tuple[bool, str]:
        module_filepath = module_filepath or f"{self._module_name}.mod"
        module_text_data = self.generate_module_text()
        try:
            self._write_to_file(module_text_data, module_filepath)
            return (True, "")
        except Exception as exc:
            return (False, exc)

    def generate_module_text(self) -> List[str]:
        module = self._generate_module_codeblock()
        return module.generate_text_list()

    def _generate_module_codeblock(self) -> CodeBlock:
        module_declaration = f"MODULE {self._module_name}\n"
        module_end = "ENDMODULE\n"
        tool = self._generate_tooldata_line()
        procedure = self._generate_procedure_codeblock()
        code = [[tool], self._robtargets, procedure]
        return CodeBlock(start_line=module_declaration, end_line=module_end, code=code)

    def _generate_tooldata_line(self) -> str:
        tool_data = self._tool.data
        rob_hold = tool_data.robhold
        tframe = tool_data.tframe
        tload = tool_data.tload

        tooldata_str = f"[{rob_hold},[{tframe.trans},{tframe.rot}],[{tload.mass},{tload.cog},{tload.aom},{tload.ix},{tload.iy},{tload.iz}]]"

        return f"PERS tooldata {self._tool.name}:={tooldata_str};\n"

    def _generate_procedure_codeblock(self) -> CodeBlock:
        procedure_declaration = f"PROC {self._procedure_name}()\n"
        procedure_close = "ENDPROC\n"
        return CodeBlock(
            start_line=procedure_declaration,
            end_line=procedure_close,
            code=[self._move_commands],
        )

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
            logger.info(f"writing to {filepath}...")
            for line in data:
                file.writelines(line)
