import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from gcode_to_robot_code.constants import CartesianCoordinate, CartesianCoordinateAxis
from gcode_to_robot_code.model import ObjectPathModel


class TestObjectModel:
    def setup_method(self):
        initial_pathdata = [
            {
                CartesianCoordinateAxis.X: 1.0,
                CartesianCoordinateAxis.Y: 2.0,
                CartesianCoordinateAxis.Z: 3.0,
            }
        ]
        self.model = ObjectPathModel(initial_pathdata)

    def test_add_point(self):
        coordinate = CartesianCoordinate(4.0, 5.0, 6.0)
        self.model.add_point(coordinate)

        expected_model = pd.DataFrame(
            [
                {
                    CartesianCoordinateAxis.X: 1.0,
                    CartesianCoordinateAxis.Y: 2.0,
                    CartesianCoordinateAxis.Z: 3.0,
                },
                {
                    CartesianCoordinateAxis.X: 4.0,
                    CartesianCoordinateAxis.Y: 5.0,
                    CartesianCoordinateAxis.Z: 6.0,
                },
            ]
        )
        assert_frame_equal(self.model.toolpath, expected_model)

    def test_get_point(self):
        coordinate = self.model.get_point(0)
        assert coordinate == CartesianCoordinate(1, 2, 3)

    def test_x_property(self):
        x_series = self.model.x
        expected_x_series = pd.Series([1.0], name=CartesianCoordinateAxis.X)
        assert_series_equal(x_series, expected_x_series)

    def test_y_property(self):
        y_series = self.model.y
        expected_y_series = pd.Series([2.0], name=CartesianCoordinateAxis.Y)
        assert_series_equal(y_series, expected_y_series)

    def test_z_property(self):
        z_series = self.model.z
        ezpected_z_series = pd.Series([3.0], name=CartesianCoordinateAxis.Z)
        assert_series_equal(z_series, ezpected_z_series)

    def test_remove_point(self):
        self.model.remove_point_by_index(0)
        assert self.model.pathlength == 0

    def test_subset_model(self):
        pathdata = [
            {
                CartesianCoordinateAxis.X: 1.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 2.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 3.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 4.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 5.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 6.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 7.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 8.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 9.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
            {
                CartesianCoordinateAxis.X: 10.0,
                CartesianCoordinateAxis.Y: 1.0,
                CartesianCoordinateAxis.Z: 1.0,
            },
        ]
        self.model = ObjectPathModel(pathdata)
        self.model.subset_model(50)

        expected_model = pd.DataFrame(
            [
                {
                    CartesianCoordinateAxis.X: 1.0,
                    CartesianCoordinateAxis.Y: 1.0,
                    CartesianCoordinateAxis.Z: 1.0,
                },
                {
                    CartesianCoordinateAxis.X: 3.0,
                    CartesianCoordinateAxis.Y: 1.0,
                    CartesianCoordinateAxis.Z: 1.0,
                },
                {
                    CartesianCoordinateAxis.X: 5.0,
                    CartesianCoordinateAxis.Y: 1.0,
                    CartesianCoordinateAxis.Z: 1.0,
                },
                {
                    CartesianCoordinateAxis.X: 7.0,
                    CartesianCoordinateAxis.Y: 1.0,
                    CartesianCoordinateAxis.Z: 1.0,
                },
                {
                    CartesianCoordinateAxis.X: 9.0,
                    CartesianCoordinateAxis.Y: 1.0,
                    CartesianCoordinateAxis.Z: 1.0,
                },
            ]
        )

        assert_frame_equal(self.model.toolpath, expected_model)

    def test_from_coordinates(self):
        coordinates = [
            {
                CartesianCoordinateAxis.X: 10.0,
                CartesianCoordinateAxis.Y: 20.0,
                CartesianCoordinateAxis.Z: 30.0,
            },
        ]
        toolpath = ObjectPathModel.from_coordinates(coordinates)
        assert toolpath.x[0] == 10.0
        assert toolpath.y[0] == 20.0
        assert toolpath.z[0] == 30.0

    def test_optimize_path(self):
        coordinates = [
            {
                CartesianCoordinateAxis.X: 10.0,
                CartesianCoordinateAxis.Y: 10.0,
                CartesianCoordinateAxis.Z: 10.0,
            },
            {
                CartesianCoordinateAxis.X: 20.0,
                CartesianCoordinateAxis.Y: 10.0,
                CartesianCoordinateAxis.Z: 10.0,
            },
            {
                CartesianCoordinateAxis.X: 30.0,
                CartesianCoordinateAxis.Y: 10.0,
                CartesianCoordinateAxis.Z: 10.0,
            },
        ]
        toolpath = ObjectPathModel.from_coordinates(coordinates)
        toolpath.optimize_straight_line()
        assert toolpath.pathlength == 2
