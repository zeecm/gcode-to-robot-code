from enum import Enum
from typing import List, NamedTuple

from gcode_to_robot_code.constants import CartesianCoordinate

# source: https://pypi.org/project/abb-motion-program-exec/


class SpeedData(NamedTuple):
    v_tcp: float
    v_ori: float
    v_leax: float
    v_reax: float


class ZoneData(NamedTuple):
    finep: bool
    pzone_tcp: float
    pzone_ori: float
    pzone_eax: float
    zone_ori: float
    zone_leax: float
    zone_reax: float


class JointTarget(NamedTuple):
    robax: List[float]  # shape=(6,)
    extax: List[float]  # shape=(6,)


class Pose(NamedTuple):
    trans: List[float]  # [x,y,z]
    rot: List[float]  # [qw,qx,qy,qz]


class ConfData(NamedTuple):
    cf1: float
    cf4: float
    cf6: float
    cfx: float


class RobTarget(NamedTuple):
    trans: CartesianCoordinate  # [x,y,z]
    rot: List[float]  # [qw,qx,qy,qz]
    robconf: ConfData  #
    extax: str  # shape=(6,)

    def to_string(self) -> str:
        return f"[{list(self.trans)}, {self.rot},{list(self.robconf)}, {self.extax}]"


class LoadData(NamedTuple):
    mass: float
    cog: List[float]  # shape=(3,)
    aom: List[float]  # shape=(4,)
    ix: float
    iy: float
    iz: float


class ToolData(NamedTuple):
    robhold: bool
    tframe: Pose
    tload: LoadData


class ToolInfo(NamedTuple):
    name: str
    data: ToolData


class PredefinedSpeed(Enum):
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
    LINEAR = "moveL"
    PATHFINDING = "moveJ"
    CURVE = "moveC"
