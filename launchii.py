"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
import sys
import platform

import cli
import gui

import appsearch
import macappsearch

def searcher(system):
    return appsearch if system == "Windows" else macappsearch

def main(cli, gui, print, args, searcher):
    if "--cli" in args:
        cli.main(searcher)
    elif "--gui" in args:
        gui.main(searcher)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(cli, gui, print, sys.argv, searcher(platform.system()))
