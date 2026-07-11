import shlex
import subprocess
import sys
import tomllib
from argparse import Namespace
from pathlib import Path

from trun.data import CONFIG_FILES, TOOLS, get_config_path_args, resolve_config_dir


def init(config_dir: Path):
    move(config_dir, force=True)
    trun_toml = config_dir / "trun.toml"
    trun_toml.touch()
    trun_toml.write_text("""lint = ["pre-commit run --all-files"]
fix = ["ruff check --fix", "ruff format"]
commit = ["git add .", "pre-commit run"]
""")


def move(config_dir: Path, force: bool = False):
    config_dir.mkdir(exist_ok=True)

    for filename in CONFIG_FILES:
        file = Path(filename)
        if not file.exists():
            continue

        dst = config_dir / file.name
        if not dst.exists() or force:
            file.replace(config_dir / file)
            print(f"Moved {filename} to {config_dir}")
        else:
            print(f"{dst} already exists")


def run_group(config_dir: Path, group_name: str):
    with open(config_dir / "trun.toml", "rb") as f:
        config = tomllib.load(f)
    group = config[group_name.lower()]
    for cmd in group:
        cmd_args = shlex.split(cmd)
        run_tool(cmd_args[0], *cmd_args[1:])


def run_tool(tool_name: str, *extra_args):
    args = [tool_name, *extra_args]
    if tool_name in TOOLS:
        args.extend(get_config_path_args(tool_name))
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


def handle_command(args: Namespace):
    cdir = resolve_config_dir()
    match args.command:
        case "init":
            init(cdir)
        case "move":
            move(cdir, force=args.force)
        case "run":
            run_group(cdir, group_name=args.group)
