.PHONY: validate lint format format-check

validate:
	uv run mypy

lint:
	uv run pylint -j4 visualizer

format:
	uv run black visualizer

format-check:
	uv run black --check visualizer