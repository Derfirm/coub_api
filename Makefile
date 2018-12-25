.PHONY: clean
clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@rm -rf build dist .coverage MANIFEST

.PHONY: test
test:
	@poetry run py.test --cov-report term-missing --cov=coub_api tests/

.PHONY: lint-flake8
flake8:
	@poetry run flake8 coub_api tests

.PHONY: lint-isort
isort:
	@poetry run isort -rc --diff coub_api

.PHONY: lint-mypy
lint-mypy:
	@poetry run mypy coub_api

.PHONY: lint
lint: lint-isort lint-flake8 lint-mypy

.PHONY: check
check: lint test