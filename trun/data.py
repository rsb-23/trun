import textwrap
import tomllib
from functools import lru_cache
from importlib.metadata import version
from pathlib import Path

VERSION = "v" + version("t-run")
DEFAULT_CONFIG_DIR = "1_config"

CONFIG_FILES = (".flake8", ".pre-commit-config.yaml", ".pylintrc", "mypy.ini", "ruff.toml", "tox.ini")
TOOLS = {
    "black": ("--config", "pyproject.toml"),
    "flake8": ("--config", ".flake8"),
    "isort": ("--settings-path ", ""),
    "mypy": ("--config", "mypy.ini"),
    "pre-commit": ("--config", ".pre-commit-config.yaml"),
    "pylint": ("--rcfile", ".pylintrc"),
    "ruff": ("--config", "ruff.toml"),
}

_indent = " " * 6
USAGE_TEXT = f"""T-run {VERSION}

Usage: 1. trun <move, --version, --help> [args...]
       2. trun <tool-name> [args...]

Supported tools:
{textwrap.fill(", ".join(TOOLS), initial_indent=_indent, subsequent_indent=_indent)}
"""


@lru_cache(3)
def resolve_config_dir() -> Path:
    cfg = tomllib.loads(Path("pyproject.toml").read_text())
    return Path(cfg.get("tool", {}).get("config-dir", DEFAULT_CONFIG_DIR))


def get_config_path_args(key) -> tuple[str, Path]:
    cdir = resolve_config_dir()
    option, file = TOOLS[key]
    cfg_file = cdir / file
    if not cfg_file.exists():
        raise FileNotFoundError(cfg_file)
    return option, cfg_file
