
install-poetry:
	python3 -m pip install poetry

install-tools:	install-poetry

setup: install-tools sync

sync_deps:
	poetry install --no-root

sync: sync_deps poetry_lock

poetry_lock:
	poetry lock --no-update

run:
	poetry run python3 -m game

clean-venv:
	rm -rf .venv

format:
	poetry run ruff format

lint:
	poetry run ruff check --fix

clean: clean-venv

.PHONY: setup install-tools setup sync_deps sync poetry_lock run clean-venv clean