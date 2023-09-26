from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd
from loguru import logger

from gcode_to_robot_code.constants import Coordinate, ProjectionMode
from gcode_to_robot_code.path_plotter import MatplotlibPathPlotter, PathPlotter


class ObjectModel:
    def __init__(self, pathdata: Optional[List[Dict[str, float]]] = None):
        if not pathdata:
            self._pathdata = pd.DataFrame(columns=["x", "y", "z"])
        else:
            self._pathdata = pd.DataFrame(pathdata)
        self._pathdata.astype(float, copy=False)

    @property
    def pathlength(self) -> int:
        return len(self._pathdata.index)

    @property
    def x(self) -> pd.Series:
        return self._pathdata["x"]

    @property
    def y(self) -> pd.Series:
        return self._pathdata["y"]

    @property
    def z(self) -> pd.Series:
        return self._pathdata["z"]

    @property
    def model(self) -> pd.DataFrame:
        return self._pathdata

    def add_point(
        self, coordinate: Coordinate, before_index: Optional[int] = None
    ) -> None:
        new_point = [coordinate.x, coordinate.y, coordinate.z]
        if before_index:
            mid_index = before_index - 0.5
            self._pathdata.loc[mid_index, :] = new_point
        else:
            last_index = self.pathlength
            self._pathdata.loc[last_index, :] = new_point
        self._pathdata.reset_index(drop=True, inplace=True)

    def get_point(self, index: int) -> Coordinate:
        point_row = self._pathdata.iloc[index]
        x = point_row["x"]
        y = point_row["y"]
        z = point_row["z"]
        return Coordinate(x, y, z)

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
        plotter: Optional[PathPlotter] = None,
        projection: ProjectionMode = ProjectionMode.TWO_DIMENSIONAL,
    ) -> None:
        plotter = plotter or MatplotlibPathPlotter()
        x = self.x.to_numpy()
        y = self.y.to_numpy()
        z = self.z.to_numpy()
        plotter.plot_path(x=x, y=y, z=z, projection=projection)

    @classmethod
    def model_from_coordinates(cls, pathdata: List[Dict[str, float]]) -> ObjectModel:
        return ObjectModel(pathdata)