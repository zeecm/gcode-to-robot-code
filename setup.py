from setuptools import find_packages, setup

PACKAGE = "gcode_to_robot_code"

setup(
    name="gcode-to-robot-code",
    version="0.0.1",
    packages=find_packages(include=PACKAGE),
    install_requires=[
        "pandas",
        "numpy",
        "python-dotenv",
        "requests",
        "loguru",
        "matplotlib",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "pycln",
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "radon",
            "codespell",
            "pre-commit",
            "pyright",
            "pylint",
            "pandas-stubs",
        ]
    },
)
