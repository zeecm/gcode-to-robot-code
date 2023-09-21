.PHONY: install format check test

PACKAGE = "gcode_to_robot_code"

install:
	pip install -e .[dev]
	pre-commit autoupdate
	pre-commit install

check:
	-pylint $(PACKAGE)
	pyright $(PACKAGE) tests/

test:
	pytest --cov=$(PACKAGE) tests/

format:
	pycln .
	black .
	isort .
