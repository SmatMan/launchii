"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
import sys

import cli
import gui


def main(cli, gui, print, args):
    if "--cli" in args:
        cli.main()
    elif "--gui" in args:
        gui.main()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(cli, gui, print, sys.argv)
