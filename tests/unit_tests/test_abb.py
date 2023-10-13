from typing import List

import pytest

from gcode_to_robot_code.abb.abb_data_types import ConfData, RobTarget
from gcode_to_robot_code.abb.abb_generator import CodeBlock
from gcode_to_robot_code.constants import CartesianCoordinate


@pytest.mark.parametrize(
    "codeblock, expected_text_list",
    [
        (
            CodeBlock(
                start_line="PROC TestProc()",
                end_line="ENDPROC",
                code=[
                    [
                        r"moveJ zcHome,v1000,fine,tool1\WObj:=wobj0;",
                        r"moveJ p_DrawEllipse_0,v500,fine,tool1\WObj:=wobj0;",
                    ]
                ],
            ),
            [
                "PROC TestProc()",
                r"    moveJ zcHome,v1000,fine,tool1\WObj:=wobj0;",
                r"    moveJ p_DrawEllipse_0,v500,fine,tool1\WObj:=wobj0;",
                "\n",
                "ENDPROC",
            ],
        ),
        (
            CodeBlock(
                start_line="MODULE TestModule",
                end_line="ENDMODULE",
                code=[
                    [
                        "CONST robtarget zcHome := [[650.0, 0.0, 1000.0], [-1.0, 0.0, 0.0, 0.0],[-1.0, 0.0, 1.0, 0.0], [9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]];",
                        "CONST robtarget p_DrawEllipse_0 := [[1117.196, -30.415, 430.2], [-1.0, 0.0, 0.0, 0.0],[-1.0, 0.0, 1.0, 0.0], [9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]];",
                    ],
                    CodeBlock(
                        start_line="PROC TestProc()",
                        end_line="ENDPROC",
                        code=[
                            [
                                r"moveJ zcHome,v1000,fine,tool1\WObj:=wobj0;",
                                r"moveJ p_DrawEllipse_0,v500,fine,tool1\WObj:=wobj0;",
                            ]
                        ],
                    ),
                ],
            ),
            [
                "MODULE TestModule",
                "    CONST robtarget zcHome := [[650.0, 0.0, 1000.0], [-1.0, 0.0, 0.0, 0.0],[-1.0, 0.0, 1.0, 0.0], [9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]];",
                "    CONST robtarget p_DrawEllipse_0 := [[1117.196, -30.415, 430.2], [-1.0, 0.0, 0.0, 0.0],[-1.0, 0.0, 1.0, 0.0], [9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]];",
                "\n",
                "    PROC TestProc()",
                "        moveJ zcHome,v1000,fine,tool1\WObj:=wobj0;",
                "        moveJ p_DrawEllipse_0,v500,fine,tool1\WObj:=wobj0;",
                "    \n",
                "    ENDPROC",
                "\n",
                "ENDMODULE",
            ],
        ),
    ],
)
def test_code_block_generated_text(codeblock: CodeBlock, expected_text_list: List[str]):
    text_list = codeblock.generate_text_list()
    assert text_list == expected_text_list


@pytest.mark.parametrize(
    "robtarget, expected_string",
    [
        (
            RobTarget(
                trans=CartesianCoordinate(650.0, 0.0, 1000.0),
                rot=[-1.0, 0.0, 0.0, 0.0],
                robconf=ConfData(
                    -1.0,
                    0.0,
                    1.0,
                    0.0,
                ),
                extax="[9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]",
            ),
            "[[650.0, 0.0, 1000.0], [-1.0, 0.0, 0.0, 0.0],[-1.0, 0.0, 1.0, 0.0], [9E+9, 9E+9, 9E9, 9E9, 9E9, 9E9]]",
        )
    ],
)
def test_robtarget_to_string(robtarget: RobTarget, expected_string: str):
    robtarget_str = robtarget.to_string()
    assert robtarget_str == expected_string
