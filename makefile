.PHONY: test, lint, mypy, lock

lock:
	uv pip compile pyproject.toml --extra server --extra evaluator --extra dev -o requirements.txt && uv cache clean

venv:
	uv venv
	uv pip sync requirements.txt && \
	bash -c 'source $(CURDIR)/.venv/bin/activate' && \
	uv pip install -e . --no-deps && \
	uv pip install --upgrade pip
