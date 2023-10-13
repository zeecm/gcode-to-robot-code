# Convert GCODE to Robotic Code
-

```
gcode-to-robot-code
│
├─ .github
│  └─ workflows
│     └─ check_and_test.yaml
├─ .gitignore
├─ .pre-commit-config.yaml
├─ Makefile
├─ README.md
├─ gcode_to_robot_code
│  ├─ __init__.py
│  ├─ abb
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ data_types.py
│  │  └─ gcode_to_abb.py
│  ├─ constants.py
│  ├─ gcode_files
│  │  ├─ cylinder.gcode
│  │  ├─ cylinder_v2.gcode
│  │  └─ mencast_logo.gcode
│  ├─ gcode_reader.py
│  ├─ model.py
│  └─ path_plotter.py
├─ pyproject.toml
├─ setup.py
└─ tests
   ├─ __init__.py
   ├─ test_gcode_reader.py
   ├─ test_model.py
   └─ test_path_plotter.py

```