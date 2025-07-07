export PYTHONPATH := $(PWD)

.PHONY: test test-cov

test:
	pytest -v

test-cov:
	pytest --cov=mercearia --cov-report=term-missing -v