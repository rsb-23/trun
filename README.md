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

## Quickstart

```bash
pipx install t-run # global
trun init
trun black .
```

## Usage

### To run individual commands

```bash
trun black .
trun pre-commit run
trun pylint *
trun ruff check .
```

### To run command groups

Add groups of command in `trun.toml` and run using `trun run`

```toml
lint = ["pre-commit run --all-files"]
fix = ["ruff check --fix", "ruff format"]
```

```commandline
trun run lint
trun run fix
```

## pre-commit

```yaml
repos:
  - repo: https://github.com/rsb-23/trun
    rev: v0.0.4
    hooks:
      - id: black
      - id: isort
      - id: flake8
      - id: ...
```

Only the hooks you list are installed — each pulls its own pinned
dependency via `additional_dependencies` in `.pre-commit-hooks.yaml`.

## Build

```bash
pip install --group build
python -m build
```

## License

MIT
