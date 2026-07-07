# T-run (Tool Run)

Config-dir-aware CLI wrapper and pre-commit hook dispatcher.

Reads a `config-dir` setting from `pyproject.toml` and routes tools
(ruff, black, isort, mypy, flake8, pylint) to look for their config
files there, instead of the project root.

## pyproject.toml

```toml
[tool]
config-dir = "config"   # default: "1_config"
```

## Install

```bash
pipx install t-run # global
```

## Usage

```bash
trun ruff check .
trun black .
trun mypy .
trun isort .
trun flake8 .
trun pylint *
```

Or without installing, from the repo root:

```bash
python -m trun ruff .
```

## pre-commit

```yaml
repos:
  - repo: https://github.com/rsb-23/trun
    rev: v0.1.0
    hooks:
      - id: ruff-check
      - id: ruff-format
      - id: black
      - id: isort
      - id: mypy
```

Only the hooks you list are installed — each pulls its own pinned
dependency via `additional_dependencies` in `.pre-commit-hooks.yaml`.

## Build

```bash
pip install build
git tag v0.1.0
python -m build
```

## License

MIT
