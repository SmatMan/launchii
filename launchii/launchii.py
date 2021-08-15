"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
import sys
import platform

import launchii.cli
import launchii.gui

import launchii.appsearch
import launchii.macappsearch

def searcher(system):
    return launchii.appsearch if system == "Windows" else launchii.macappsearch

def main(cli, gui, print, args, searcher):
    if "--cli" in args:
        cli.main(searcher)
    elif "--gui" in args:
        gui.main(searcher)
    else:
        print(__doc__)

def run():
    main(launchii.cli, launchii.gui, print, sys.argv, searcher(platform.system()))