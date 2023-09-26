import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from gcode_to_robot_code.constants import Coordinate
from gcode_to_robot_code.model import ObjectModel


class TestObjectModel:
    def setup_method(self):
        initial_pathdata = [{"x": 1.0, "y": 2.0, "z": 3.0}]
        self.model = ObjectModel(initial_pathdata)

    def test_add_point(self):
        coordinate = Coordinate(4.0, 5.0, 6.0)
        self.model.add_point(coordinate)

        expected_model = pd.DataFrame(
            [
                {"x": 1.0, "y": 2.0, "z": 3.0},
                {"x": 4.0, "y": 5.0, "z": 6.0},
            ]
        )
        assert_frame_equal(self.model.model, expected_model)

    def test_get_point(self):
        coordinate = self.model.get_point(0)
        assert coordinate == Coordinate(1, 2, 3)

    def test_x_property(self):
        x_series = self.model.x
        expected_x_series = pd.Series([1.0], name="x")
        assert_series_equal(x_series, expected_x_series)

    def test_y_property(self):
        y_series = self.model.y
        expected_y_series = pd.Series([2.0],name="y")
        assert_series_equal(y_series, expected_y_series)

    def test_z_property(self):
        z_series = self.model.z
        ezpected_z_series = pd.Series([3.0], name="z")
        assert_series_equal(z_series, ezpected_z_series)
        
    def test_remove_point(self):
        self.model.remove_point_by_index(0)
        assert self.model.pathlength == 0

    def test_subset_model(self):
        pathdata = [
            {"x": 1.0, "y": 1.0, "z": 1.0},
            {"x": 2.0, "y": 1.0, "z": 1.0},
            {"x": 3.0, "y": 1.0, "z": 1.0},
            {"x": 4.0, "y": 1.0, "z": 1.0},
            {"x": 5.0, "y": 1.0, "z": 1.0},
            {"x": 6.0, "y": 1.0, "z": 1.0},
            {"x": 7.0, "y": 1.0, "z": 1.0},
            {"x": 8.0, "y": 1.0, "z": 1.0},
            {"x": 9.0, "y": 1.0, "z": 1.0},
            {"x": 10.0, "y": 1.0, "z": 1.0},
        ]
        self.model = ObjectModel(pathdata)
        self.model.subset_model(50)
        
        expected_model = pd.DataFrame(
            [
            {"x": 1.0, "y": 1.0, "z": 1.0},
            {"x": 3.0, "y": 1.0, "z": 1.0},
            {"x": 5.0, "y": 1.0, "z": 1.0},
            {"x": 7.0, "y": 1.0, "z": 1.0},
            {"x": 9.0, "y": 1.0, "z": 1.0},
        ]
        )
        
        assert_frame_equal(self.model.model, expected_model)
        