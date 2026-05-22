.PHONY: venv install test

venv:
	python3 -m venv .venv

install: venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:
	.venv/bin/pytest
