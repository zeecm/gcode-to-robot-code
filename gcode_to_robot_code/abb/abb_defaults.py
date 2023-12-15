"""
This code initializes default values for various ABB robot data types and constants used in the gcode_to_robot_code module.

The code imports several data types and constants from the gcode_to_robot_code.abb.abb_data_types and gcode_to_robot_code.constants modules. It then defines default values for tool data, tool name, offset, rotation, configuration data, external axes, and home coordinate. These default values are used as initial values or fallback values in the gcode_to_robot_code module.
"""

from gcode_to_robot_code.abb.abb_data_types import (
    ConfData,
    LoadData,
    Pose,
    RobTarget,
    ToolData,
    ToolInfo,
)
from gcode_to_robot_code.constants import CartesianCoordinate

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
