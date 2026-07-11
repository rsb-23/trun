import argparse
import sys

from trun.commands import handle_command, run_tool
from trun.data import TOOLS, VERSION


def main():
    parser = argparse.ArgumentParser(description="Config path aware tool runner")
    parser.add_argument("-v", "--version", action="version", version=f"T-run {VERSION}")
    # parser.add_help
    subparsers = parser.add_subparsers(dest="command")

    # 1. Dynamically register all commands
    for cmd in TOOLS:
        subparsers.add_parser(cmd)

    subparsers.add_parser("init", help="Do tool setup")
    move_parser = subparsers.add_parser("move", help="Move supported configs (like .flake8) to config-dir")
    move_parser.add_argument("--force", "-f", action="store_true", help="Force the move operation")

    run_parser = subparsers.add_parser("run", help="Run the commands from trun.toml")
    run_parser.add_argument("group", help="Group of commands to run")

    args, extra_args = parser.parse_known_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd = args.command
    if cmd not in TOOLS:
        handle_command(args)
        sys.exit(0)

    run_tool(cmd, *extra_args)


if __name__ == "__main__":
    main()
