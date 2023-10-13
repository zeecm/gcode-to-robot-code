from typing import List, NamedTuple

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe"""

    def __init__(
        self,
        dataframe: pd.DataFrame,
        show_index: bool = False,
        show_headers: bool = True,
        parent=None,
    ):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe
        self._show_index = show_index
        self._show_headers = show_headers

    def rowCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        return len(self._dataframe) if parent == QModelIndex() else 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        return len(self._dataframe.columns) if parent == QModelIndex() else 0

    def data(
        self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return (
                    str(self._dataframe.columns[section])
                    if self._show_headers
                    else None
                )

            if orientation == Qt.Orientation.Vertical:
                return str(self._dataframe.index[section]) if self._show_index else None

        return None

    def get_data(self, view: bool = True) -> pd.DataFrame:
        return self._dataframe if view else self._dataframe.copy()


class DialogFileType(NamedTuple):
    filetype_name: str
    extensions: List[str]

    @property
    def pyside6_filter_str(self):
        formatted_extensions = [
            "*." + ext.strip().strip(".") for ext in self.extensions
        ]
        return f"{self.filetype_name} ({' '.join(formatted_extensions)})"
