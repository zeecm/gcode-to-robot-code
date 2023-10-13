from gcode_to_robot_code.abb.data_types import (
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
