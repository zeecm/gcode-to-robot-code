from typing import List

import pytest

from gcode_to_robot_code.gui.gui_classes import DialogFileType


@pytest.mark.parametrize(
    "title, extensions, expected_pyside6_filter_str",
    [
        ("Gcode Files", ["gcode"], "Gcode Files (*.gcode)"),
        (
            "Image Files",
            [".png", "jpeg", " .wepb"],
            "Image Files (*.png *.jpeg *.wepb)",
        ),
    ],
)
def test_dialog_filetype_namedtuple(
    title: str, extensions: List[str], expected_pyside6_filter_str: str
):
    dialog_filetype = DialogFileType(title, extensions)
    assert dialog_filetype.pyside6_filter_str == expected_pyside6_filter_str
