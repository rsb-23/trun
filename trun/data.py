import tomllib
from functools import lru_cache
from pathlib import Path

DEFAULT_CONFIG_DIR = "1_config"
# key -> (executable, fn(config_dir) -> prefix args, BEFORE file args)
COMMANDS = {
    "black": "--config {}/pyproject.toml",
    "flake8": "--config {}/.flake8",
    "isort": "--settings-path {}",
    "mypy": "--config-file {}/mypy.ini",
    "pre-commit": "--config {}\\.pre-commit-config.yaml",
    "pylint": "--rcfile {}/.pylintrc",
    "ruff": "--config {}/ruff.toml",
}


@lru_cache(3)
def resolve_config_dir() -> Path:
    cfg = tomllib.loads(Path("pyproject.toml").read_text())
    return Path(cfg.get("tool", {}).get("config-dir", DEFAULT_CONFIG_DIR))


def get_config_path_args(key) -> list[str]:
    cdir = resolve_config_dir()
    return COMMANDS[key].format(cdir).split()
