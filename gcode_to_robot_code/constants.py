"""
This code defines several data types related to Cartesian coordinates, including an enumeration for projection modes and an enumeration for Cartesian coordinate axes. It also defines a CartesianCoordinate named tuple that represents a point in 3D space and provides methods for offsetting the coordinates.

The code defines the following:

ProjectionMode enum: Represents different projection modes, either three-dimensional or two-dimensional.
CartesianCoordinateAxis enum: Represents different Cartesian coordinate axes, either X, Y, or Z.
CartesianCoordinate named tuple: Represents a point in 3D space with x, y, and z coordinates. It provides two methods:
offset_by_coordinate: Offsets the coordinates by another CartesianCoordinate object.
offset_by_values: Offsets the coordinates by individual x, y, and z values.
"""


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
        self, x_offset: float = 0.0, y_offset: float = 0.0, z_offset: float = 0.0
    ) -> CartesianCoordinate:
        return CartesianCoordinate(
            self.x + x_offset, self.y + y_offset, self.z + z_offset
        )
