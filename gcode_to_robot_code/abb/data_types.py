from typing import List, NamedTuple

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
    trans: List[float]  # [x,y,z]
    rot: List[float]  # [qw,qx,qy,qz]
    robconf: ConfData  #
    extax: List[float]  # shape=(6,)


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
