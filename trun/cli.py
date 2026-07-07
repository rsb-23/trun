import os
import sys

from .data import COMMANDS, get_config_path_args


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        keys = ", ".join(COMMANDS)
        print(f"usage: confdir <{keys}> [args...]", file=sys.stderr)
        sys.exit(2)

    cmd, *rest = sys.argv[1:]
    cmd = cmd.lower()
    os.execvp(cmd, [cmd, *rest, *get_config_path_args(cmd)])


if __name__ == "__main__":
    main()
