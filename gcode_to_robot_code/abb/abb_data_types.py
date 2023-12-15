from enum import Enum
from typing import List, NamedTuple

from gcode_to_robot_code.constants import CartesianCoordinate

# source: https://pypi.org/project/abb-motion-program-exec/


class SpeedData(NamedTuple):
    """
    This code defines a named tuple SpeedData that represents speed data for a robot. It has four fields: v_tcp, v_ori, v_leax, and v_reax.

    The SpeedData named tuple is defined using the NamedTuple class from the typing module. It has four fields, each representing a different type of speed data for a robot.
    """

    v_tcp: float
    v_ori: float
    v_leax: float
    v_reax: float


class ZoneData(NamedTuple):
    """
    This code defines a named tuple ZoneData that represents zone data for a robot. It has seven fields: finep, pzone_tcp, pzone_ori, pzone_eax, zone_ori, zone_leax, and zone_reax.

    The ZoneData named tuple is defined using the NamedTuple class from the typing module. It has seven fields, each representing a different type of zone data for a robot.
    """

    finep: bool
    pzone_tcp: float
    pzone_ori: float
    pzone_eax: float
    zone_ori: float
    zone_leax: float
    zone_reax: float


class JointTarget(NamedTuple):
    """
    This code defines a named tuple JointTarget that represents a joint target for a robot. It has two fields: robax and extax, which are lists of floats representing the robot axes and external axes, respectively.

    The JointTarget named tuple is defined using the NamedTuple class from the typing module. It has two fields, robax and extax, which are lists of floats representing the robot axes and external axes, respectively.
    """

    robax: List[float]  # shape=(6,)
    extax: List[float]  # shape=(6,)


class Pose(NamedTuple):
    """
    This code defines a named tuple Pose that represents a pose in 3D space. It has two fields: trans and rot, which are lists of floats representing the translation and rotation components of the pose, respectively.

    The Pose named tuple is defined using the NamedTuple class from the typing module. It has two fields, trans and rot, which are lists of floats representing the translation and rotation components of the pose, respectively.
    """

    trans: List[float]  # [x,y,z]
    rot: List[float]  # [qw,qx,qy,qz]


class ConfData(NamedTuple):
    """
    This code defines a named tuple ConfData that represents configuration data for a robot. It has four fields: cf1, cf4, cf6, and cfx, which are floats representing different configuration values.

    The ConfData named tuple is defined using the NamedTuple class from the typing module. It has four fields, each representing a different configuration value for a robot.
    """

    cf1: float
    cf4: float
    cf6: float
    cfx: float


class RobTarget(NamedTuple):
    """
    This code defines a named tuple RobTarget that represents a robot target. It has four fields: trans, rot, robconf, and extax. The RobTarget class also provides a to_string method that converts the target to a string representation.

    The RobTarget named tuple is defined using the NamedTuple class from the typing module. It has four fields: trans, rot, robconf, and extax. The trans field represents the translation components of the target, the rot field represents the rotation components, the robconf field represents the configuration data, and the extax field represents the external axes.

    The RobTarget class also provides a to_string method that converts the target to a string representation. The method uses string formatting to create a string representation of the target's fields.
    """

    trans: CartesianCoordinate  # [x,y,z]
    rot: List[float]  # [qw,qx,qy,qz]
    robconf: ConfData  #
    extax: str  # shape=(6,)

    def to_string(self) -> str:
        return f"[{list(self.trans)}, {self.rot},{list(self.robconf)}, {self.extax}]"


class LoadData(NamedTuple):
    """
    The `LoadData` class represents load data for a robot.

    Args:
        mass (float): The mass of the load.
        cog (List[float]): The center of gravity of the load. Shape: (3,)
        aom (List[float]): The axis of mass of the load. Shape: (4,)
        ix (float): The moment of inertia around the x-axis.
        iy (float): The moment of inertia around the y-axis.
        iz (float): The moment of inertia around the z-axis.
    """

    mass: float
    cog: List[float]  # shape=(3,)
    aom: List[float]  # shape=(4,)
    ix: float
    iy: float
    iz: float


class ToolData(NamedTuple):
    """
    The `ToolData` class represents tool data for a robot.

    Args:
        robhold (bool): Indicates whether the robot should hold the tool.
        tframe (Pose): The pose of the tool frame.
        tload (LoadData): The load data of the tool.
    """

    robhold: bool
    tframe: Pose
    tload: LoadData


class ToolInfo(NamedTuple):
    """
    The `ToolInfo` class represents information about a tool for a robot.

    Args:
        name (str): The name of the tool.
        data (ToolData): The tool data.
    """

    name: str
    data: ToolData


class PredefinedSpeed(Enum):
    """
    The `PredefinedSpeed` enum represents predefined speed values for a robot.
    """

    V5 = "v5"
    V10 = "v10"
    V20 = "v20"
    V30 = "v30"
    V40 = "v40"
    V50 = "v50"
    V60 = "v60"
    V80 = "v80"
    V100 = "v100"
    V150 = "v150"
    V200 = "v200"
    V300 = "v300"
    V400 = "v400"
    V500 = "v500"
    V600 = "v600"
    V800 = "v800"
    V1000 = "v1000"
    V1500 = "v1500"
    V2000 = "v2000"
    V2500 = "v2500"
    V3000 = "v3000"
    V4000 = "v4000"
    V5000 = "v5000"
    V6000 = "v6000"
    V7000 = "v7000"
    VMAX = "vmax"


class MoveType(Enum):
    """The `MoveType` enum represents different types of robot movements."""

    LINEAR = "moveL"
    PATHFINDING = "moveJ"
    CURVE = "moveC"
