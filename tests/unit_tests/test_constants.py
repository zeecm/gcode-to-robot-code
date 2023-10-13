import pytest

from gcode_to_robot_code.constants import CartesianCoordinate


@pytest.mark.parametrize(
    "coordinate, x_offset, y_offset, z_offset, expected_coordinate",
    [
        (
            CartesianCoordinate(1.0, 1.0, 1.0),
            1.0,
            2.0,
            3.0,
            CartesianCoordinate(2.0, 3.0, 4.0),
        ),
        (
            CartesianCoordinate(1.0, 1.0, 1.0),
            2.5,
            -10,
            4.3,
            CartesianCoordinate(3.5, -9.0, 5.3),
        ),
        (
            CartesianCoordinate(1.0, 1.0, 1.0),
            0.0,
            0.0,
            0.0,
            CartesianCoordinate(1.0, 1.0, 1.0),
        ),
    ],
)
def test_offset_coordinate_by_values(
    coordinate: CartesianCoordinate,
    x_offset: float,
    y_offset: float,
    z_offset: float,
    expected_coordinate: CartesianCoordinate,
):
    new_coordinate = coordinate.offset_by_values(
        x_offset=x_offset, y_offset=y_offset, z_offset=z_offset
    )
    assert new_coordinate == expected_coordinate


@pytest.mark.parametrize(
    "coordinate, offset_coordinate, expected_coordinate",
    [
        (
            CartesianCoordinate(1.0, 1.0, 1.0),
            CartesianCoordinate(1.0, 2.0, 3.0),
            CartesianCoordinate(2.0, 3.0, 4.0),
        ),
        (
            CartesianCoordinate(1.0, 1.0, 1.0),
            CartesianCoordinate(2.5, -10, 4.3),
            CartesianCoordinate(3.5, -9.0, 5.3),
        ),
        (
            CartesianCoordinate(1.0, 1.0, 1.0),
            CartesianCoordinate(0.0, 0.0, 0.0),
            CartesianCoordinate(1.0, 1.0, 1.0),
        ),
    ],
)
def test_offset_by_coordinate(
    coordinate: CartesianCoordinate,
    offset_coordinate: CartesianCoordinate,
    expected_coordinate: CartesianCoordinate,
):
    new_coordinate = coordinate.offset_by_coordinate(offset_coordinate)
    assert new_coordinate == expected_coordinate
