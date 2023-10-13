from __future__ import annotations

from typing import Dict, List, Literal, Optional, Tuple, Union

import pandas as pd
from loguru import logger

from gcode_to_robot_code.constants import (
    CartesianCoordinate,
    CartesianCoordinateAxis,
    ProjectionMode,
)
from gcode_to_robot_code.path_plotter import MatplotlibPathPlotter, PathPlotter


class ObjectPathModel:
    def __init__(
        self, pathdata: Optional[List[Dict[CartesianCoordinateAxis, float]]] = None
    ):
        if not pathdata:
            self._pathdata = pd.DataFrame(columns=list(CartesianCoordinateAxis))
        else:
            self._pathdata = pd.DataFrame(pathdata)
        self._pathdata.astype(float, copy=False)

    @property
    def pathlength(self) -> int:
        return len(self._pathdata.index)

    @property
    def x_values(self) -> pd.Series:
        return self._pathdata[CartesianCoordinateAxis.X]

    @property
    def y_values(self) -> pd.Series:
        return self._pathdata[CartesianCoordinateAxis.Y]

    @property
    def z_values(self) -> pd.Series:
        return self._pathdata[CartesianCoordinateAxis.Z]

    @property
    def toolpath_data(self) -> pd.DataFrame:
        return self._pathdata

    def add_point(
        self,
        coordinate: Union[Tuple[float, float, float], CartesianCoordinate],
        before_index: Optional[int] = None,
    ) -> None:
        if not isinstance(coordinate, CartesianCoordinate):
            coordinate = self._convert_to_cartesian_coordinate_datatype(coordinate)
        new_point = [coordinate.x, coordinate.y, coordinate.z]
        if before_index:
            mid_index = before_index - 0.5
            self._pathdata.loc[mid_index, :] = new_point
        else:
            last_index = self.pathlength
            self._pathdata.loc[last_index, :] = new_point
        self._pathdata.reset_index(drop=True, inplace=True)

    def _convert_to_cartesian_coordinate_datatype(
        self, coordinate: Tuple[float, float, float]
    ) -> CartesianCoordinate:
        return CartesianCoordinate(coordinate[0], coordinate[1], coordinate[2])

    def get_point(self, index: int) -> CartesianCoordinate:
        point_row = self._pathdata.iloc[index]
        # ignoring types as valid
        x = point_row[CartesianCoordinateAxis.X]  # type: ignore
        y = point_row[CartesianCoordinateAxis.Y]  # type: ignore
        z = point_row[CartesianCoordinateAxis.Z]  # type: ignore
        return CartesianCoordinate(x, y, z)

    def remove_point_by_index(
        self,
        index_to_remove: int,
    ) -> None:
        self._pathdata.drop(index_to_remove, inplace=True)
        self._pathdata.reset_index(drop=True, inplace=True)

    def subset_model(
        self,
        percentage: float,
    ) -> None:
        if not 0.0 <= percentage <= 100.0:
            raise ValueError(f"invalid percentage: {percentage}")
        decimal_percentage = percentage / 100
        num_rows_to_remain = self.pathlength * decimal_percentage
        step_size = int(self.pathlength / num_rows_to_remain)
        self._pathdata = self._pathdata.iloc[::step_size]
        self._pathdata.reset_index(drop=True, inplace=True)

    def plot_path(
        self,
        projection: Union[
            Literal["3d", "2d"], ProjectionMode
        ] = ProjectionMode.TWO_DIMENSIONAL,
        plotter: Optional[PathPlotter] = None,
    ) -> None:
        if not isinstance(projection, ProjectionMode):
            projection = ProjectionMode(projection)
        plotter = plotter or MatplotlibPathPlotter()
        x = self.x_values.to_numpy()
        y = self.y_values.to_numpy()
        z = self.z_values.to_numpy()
        plotter.plot_path(x=x, y=y, z=z, projection=projection)

    @classmethod
    def from_coordinates(
        cls, pathdata: List[Dict[CartesianCoordinateAxis, float]]
    ) -> ObjectPathModel:
        return ObjectPathModel(pathdata)

    def optimize_straight_lines(self) -> None:
        logger.info("optimizing straight line paths")
        optimized_toolpath = []
        start_index = 0

        while start_index < self.pathlength - 1:
            end_index = start_index + 1
            direction_vector = self._calculate_direction_vector(
                self.x_values[start_index : end_index + 1],
                self.y_values[start_index : end_index + 1],
                self.z_values[start_index : end_index + 1],
            )
            end_index += 1
            while (
                end_index < self.pathlength
                and self._calculate_direction_vector(
                    self.x_values[start_index : end_index + 1],
                    self.y_values[start_index : end_index + 1],
                    self.z_values[start_index : end_index + 1],
                )
                == direction_vector
            ):
                end_index += 1

            end_index = min(self.pathlength - 1, end_index)

            optimized_toolpath.append(self.toolpath_data.iloc[[start_index, end_index]])

            start_index = end_index + 1
        logger.info("optimization done")
        self._pathdata = pd.concat(optimized_toolpath).reset_index(drop=True)

    def _calculate_direction_vector(
        self, x_values: pd.Series, y_values: pd.Series, z_values: pd.Series
    ):
        dx = x_values.iloc[-1] - x_values.iloc[0]
        dy = y_values.iloc[-1] - y_values.iloc[0]
        dz = z_values.iloc[-1] - z_values.iloc[0]
        return dx, dy, dz
