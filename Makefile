.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python3 setup.py develop

.PHONY: build
build:
	python3 setup.py build

.PHONY: lint
lint:
	flake8 chaosdatadog/ tests/
	isort --check-only --profile black chaosdatadog/ tests/
	black --check --diff --line-length=80 chaosdatadog/ tests/

.PHONY: format
format:
	isort --profile black chaosdatadog/ tests/
	black --line-length=80 chaosdatadog/ tests/

.PHONY: tests
tests:
	pytest
