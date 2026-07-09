import argparse
import subprocess
import sys

from trun.commands import handle_command
from trun.data import TOOLS, VERSION, get_config_path_args


def main():
    parser = argparse.ArgumentParser(description="Config path aware tool runner")
    parser.add_argument("-v", "--version", action="version", version=f"T-run {VERSION}")
    # parser.add_help
    subparsers = parser.add_subparsers(dest="command")

    # 1. Dynamically register all commands
    for cmd in TOOLS:
        subparsers.add_parser(cmd)

    move_parser = subparsers.add_parser("move", help="Move supported configs (like .flake8) to config-dir")
    move_parser.add_argument("dir", nargs="?", help="The config directory to move the configs")
    move_parser.add_argument("--force", "-f", action="store_true", help="Force the move operation")

    args, extra_args = parser.parse_known_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd = args.command
    if cmd not in TOOLS:
        handle_command(args)
        sys.exit(0)

    args = [cmd, *extra_args, *get_config_path_args(cmd)]
    try:
        result = subprocess.run(args, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
