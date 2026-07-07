import os
import sys

from trun.commands import handle_command
from trun.data import TOOLS, USAGE_TEXT, get_config_path_args


def main():
    if len(sys.argv) < 2:
        print(USAGE_TEXT, file=sys.stderr)
        sys.exit(2)

    cmd, *rest = sys.argv[1:]
    cmd = cmd.lower()
    if cmd in TOOLS:
        os.execvp(cmd, [cmd, *rest, *get_config_path_args(cmd)])
    else:
        handle_command(cmd, rest)
    sys.exit(0)


if __name__ == "__main__":
    main()
