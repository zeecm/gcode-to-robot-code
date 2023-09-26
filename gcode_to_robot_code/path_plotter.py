from typing import Protocol

import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.figure import Figure
from numpy import ndarray

from gcode_to_robot_code.constants import ProjectionMode


class PathPlotter(Protocol):
    def plot_path(
        self, x: ndarray,
        y: ndarray,
        z: ndarray,projection: ProjectionMode = ProjectionMode.TWO_DIMENSIONAL
    ) -> None:
        ...


class MatplotlibPathPlotter:
    def plot_path(
        self,
        x: ndarray,
        y: ndarray,
        z: ndarray,
        projection: ProjectionMode = ProjectionMode.TWO_DIMENSIONAL,
    ) -> None:
        fig = plt.figure()

        if projection == ProjectionMode.TWO_DIMENSIONAL:
            logger.info("displaying 2d plot")
            self._plot_2d(fig, x, y)
        elif projection == ProjectionMode.THREE_DIMENSIONAL:
            logger.info("displaying 3d plot")
            self._plot_3d(fig, x, y, z)
        else:
            raise ValueError(f"invalid projection mode {projection}")
        plt.show()

    def _plot_2d(self, fig: Figure, x: ndarray, y: ndarray) -> None:
        ax = fig.add_subplot(111)
        ax.plot(x, y, "red")
        ax.scatter(x, y)

    def _plot_3d(self, fig: Figure, x: ndarray, y: ndarray, z: ndarray) -> None:
        ax = fig.add_subplot(projection="3d")
        ax.plot(x, y, z)
