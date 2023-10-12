from __future__ import annotations

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

    def offset_by_coordinate(
        self, offset_coordinates: CartesianCoordinate
    ) -> CartesianCoordinate:
        return CartesianCoordinate(
            self.x + offset_coordinates.x,
            self.y + offset_coordinates.y,
            self.z + offset_coordinates.z,
        )

    def offset_by_values(
        self, x: float = 0.0, y: float = 0.0, z: float = 0.0
    ) -> CartesianCoordinate:
        return CartesianCoordinate(self.x + x, self.y + y, self.z + z)
