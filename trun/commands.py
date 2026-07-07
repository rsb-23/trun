import os
import shutil
import sys

from trun.data import CONFIG_FILES, DEFAULT_CONFIG_DIR, USAGE_TEXT, VERSION


def move(config_dir: str):
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)

    for filename in CONFIG_FILES:
        if not os.path.exists(filename):
            continue
        try:
            shutil.move(filename, config_dir)
            print(f"Moved {filename} to {config_dir}")
        except shutil.Error as e:
            print(e)


def handle_command(command, args: list[str]):
    match command:
        case "--help":
            print(USAGE_TEXT)
        case "--version":
            print(f"trun v{VERSION}")
        case "move":
            cdir = args[0] if args else DEFAULT_CONFIG_DIR
            move(config_dir=cdir)
        case _:
            print(USAGE_TEXT, file=sys.stderr)
            sys.exit(2)
