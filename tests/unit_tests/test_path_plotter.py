import numpy as np
import pytest
from pytest_mock import MockerFixture

from gcode_to_robot_code.constants import ProjectionMode
from gcode_to_robot_code.path_plotter import MatplotlibPathPlotter, PathPlotter


@pytest.fixture(name="plotter")
def plotter_fixture() -> PathPlotter:
    return MatplotlibPathPlotter()


@pytest.mark.parametrize(
    "x, y, z, projection",
    [
        # Happy path tests
        (
            np.array([1, 2, 3]),
            np.array([4, 5, 6]),
            np.array([7, 8, 9]),
            ProjectionMode.TWO_DIMENSIONAL,
        ),
        (
            np.array([1, 2, 3]),
            np.array([4, 5, 6]),
            np.array([7, 8, 9]),
            ProjectionMode.THREE_DIMENSIONAL,
        ),
        # Edge cases
        (
            np.array([]),
            np.array([]),
            np.array([]),
            ProjectionMode.TWO_DIMENSIONAL,
        ),
        (
            np.array([1]),
            np.array([2]),
            np.array([3]),
            ProjectionMode.THREE_DIMENSIONAL,
        ),
    ],
    ids=[
        "2d_happy_path",
        "3d_happy_path",
        "empty_arrays",
        "single_point_3d",
    ],
)
def test_plot_path(
    plotter: PathPlotter,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    projection: ProjectionMode,
    mocker: MockerFixture,
):
    mocker.patch("matplotlib.pyplot.show")
    plotter.plot_path(x, y, z, projection)
