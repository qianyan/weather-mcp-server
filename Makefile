.PHONY: install format lint clean release run build publish publish-test

install:
	uv venv
	. .venv/bin/activate && PYTHONPATH=src uv pip install -e ".[dev]"

format:
	ruff format .

lint:
	ruff check .

clean:
	rm -rf .venv build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	. .venv/bin/activate && PYTHONPATH=src python -m weather_mcp_server.server

release:
	@if [ -z "$(version)" ]; then \
		echo "Please specify version: e.g, make release version=v0.0.1"; \
		exit 1; \
	fi
	@echo "Updating version to $(version:v%=%)"
	@python -c 'import tomli; import tomli_w; \
		data = tomli.load(open("pyproject.toml", "rb")); \
		data["project"]["version"] = "$(version:v%=%)"; \
		tomli_w.dump(data, open("pyproject.toml", "wb"))'
	@git add pyproject.toml
	@git commit -m "release: update version to $(version:v%=%)"
	@git push origin main
	@git tag $(version)
	@git push origin $(version)
	@echo "Version updated and tag pushed."

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

publish-test: build
	python -m twine upload --repository testpypi dist/* 