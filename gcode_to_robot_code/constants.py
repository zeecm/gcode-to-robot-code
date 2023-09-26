from enum import Enum
from typing import NamedTuple


class ProjectionMode(Enum):
    THREE_DIMENSIONAL = "3d"
    TWO_DIMENSIONAL = "2d"


class Coordinate(NamedTuple):
    x: float
    y: float
    z: float
