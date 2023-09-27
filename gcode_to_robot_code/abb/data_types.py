from typing import NamedTuple

import numpy as np

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
    robax: np.ndarray  # shape=(6,)
    extax: np.ndarray  # shape=(6,)


class Pose(NamedTuple):
    trans: np.ndarray  # [x,y,z]
    rot: np.ndarray  # [qw,qx,qy,qz]


class ConfData(NamedTuple):
    cf1: float
    cf4: float
    cf6: float
    cfx: float


class RobTarget(NamedTuple):
    trans: np.ndarray  # [x,y,z]
    rot: np.ndarray  # [qw,qx,qy,qz]
    robconf: ConfData  #
    extax: np.ndarray  # shape=(6,)


class LoadData(NamedTuple):
    mass: float
    cog: np.ndarray  # shape=(3,)
    aom: np.ndarray  # shape=(4,)
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
