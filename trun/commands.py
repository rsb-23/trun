from argparse import Namespace
from pathlib import Path

from trun.data import CONFIG_FILES, resolve_config_dir


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


def handle_command(args: Namespace):
    match args.command:
        case "move":
            cdir = args.dir or resolve_config_dir()
            move(config_dir=Path(cdir), force=args.force)
