# Convert GCODE to Robotic Code
-

## Setup
- If using make:
make install
- Manually:
`pip install -e .[dev]`

"
## Sample Usage:
```python
reader = GcodeReader()
model = reader.read_file("sample.gcode")
model.plot_path("2d")
model.plot_path("3d")

abb_module_generator = ABBModuleGenerator(model, module_name="SampleModule", procedure_name="DoStuff")
abb_module_generator.save_as_module("SampleModule.mod")

```

## GUI:
```python3 -m main```

## Directory Structure:

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
│  │  ├─ abb_data_types.py
│  │  ├─ abb_defaults.py
│  │  └─ abb_generator.py
│  ├─ constants.py
│  ├─ gcode_files
│  │  ├─ EllipseV3.gcode
│  │  ├─ cylinder.gcode
│  │  ├─ cylinder_v2.gcode
│  │  └─ mencast_logo.gcode
│  ├─ gcode_reader.py
│  ├─ gui
│  │  ├─ gui_classes.py
│  │  ├─ gui_window.py
│  │  └─ pyside_files
│  │     ├─ designer
│  │     │  └─ app_window.ui
│  │     └─ generated
│  │        └─ app_window.py
│  ├─ model.py
│  └─ path_plotter.py
├─ main.py
├─ pyproject.toml
├─ setup.py
└─ tests
   ├─ __init__.py
   ├─ integration_tests
   │  ├─ sample_generated_modules
   │  └─ test_abb_generator.py
   └─ unit_tests
      ├─ test_abb.py
      ├─ test_constants.py
      ├─ test_gcode_reader.py
      ├─ test_gui.py
      ├─ test_model.py
      └─ test_path_plotter.py

```