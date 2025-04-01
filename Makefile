.PHONY: install format lint clean release run build publish publish-test update-version

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

build: clean install
	. .venv/bin/activate && python -m build

publish-test: build
	. .venv/bin/activate && python -m twine upload --repository testpypi dist/*

publish: build
	. .venv/bin/activate && python -m twine upload dist/*

# 更新版本号
update-version:
	@if [ -z "$(version)" ]; then \
		echo "Please specify version: e.g, make release version=v0.0.1"; \
		exit 1; \
	fi
	@echo "Updating version to $(version:v%=%)"
	. .venv/bin/activate && python -c 'import tomli; import tomli_w; \
		data = tomli.load(open("pyproject.toml", "rb")); \
		data["project"]["version"] = "$(version:v%=%)"; \
		tomli_w.dump(data, open("pyproject.toml", "wb"))'

# 发布新版本
release: install update-version
	@git add pyproject.toml
	@git commit -m "release: update version to $(version:v%=%)"
	@git tag $(version)
	@git push origin main
	@git push origin $(version)
	@$(MAKE) publish
	@echo "✨ Version $(version) updated and published to PyPI" 