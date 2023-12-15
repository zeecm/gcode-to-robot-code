.PHONY: install format check test

PACKAGE = "gcode_to_robot_code"

install:
	pip install --upgrade pip
	pip install -e .[dev]
	pre-commit autoupdate
	pre-commit install

check:
	-pylint $(PACKAGE)
	pyright $(PACKAGE) tests/

test:
	python3 -m pytest --cov=$(PACKAGE) tests/

format:
	pycln $(PACKAGE) tests/
	black $(PACKAGE) tests/
	isort $(PACKAGE) tests/

update-qt:
	pyside6-uic gcode_to_robot_code/gui/pyside_files/designer/app_window.ui -o gcode_to_robot_code/gui/pyside_files/generated/app_window.py

run:
	python3 -m main