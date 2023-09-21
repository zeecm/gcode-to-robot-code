import pytest

from gcode_to_robot_code.template import template_add


@pytest.mark.parametrize(
    "num1, num2, result",
    [
        (1, 2, 3),
        (2, 2, 4),
        (5, 7, 12),
    ],
)
def test_template_add(num1, num2, result):
    assert template_add(num1, num2) == result
