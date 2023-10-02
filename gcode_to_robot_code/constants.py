from enum import Enum
from typing import NamedTuple


class ProjectionMode(Enum):
    THREE_DIMENSIONAL = "3d"
    TWO_DIMENSIONAL = "2d"


class CartesianCoordinateAxis(Enum):
    X = "x"
    Y = "y"
    Z = "z"


class CartesianCoordinate(NamedTuple):
    x: float
    y: float
    z: float
