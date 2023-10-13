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
