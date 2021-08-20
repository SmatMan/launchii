"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
from launchii.crosssearch import BaseSearch
import sys
import platform
import importlib
import typing as t

import launchii.cli
import launchii.gui


def get_searcher_class(module_name: str) -> t.Type[BaseSearch]:
    pieces = module_name.split(":")
    actual_module = importlib.import_module(pieces[0])
    return getattr(actual_module, pieces[1])


def searcher(system: str, packages: t.List[str]) -> BaseSearch:
    for package in packages:
        searcher_class = get_searcher_class(package)
        if searcher_class.supported_environment(system):
            return searcher_class()


def main(cli, gui, print, args, searcher):
    if "--cli" in args:
        cli.main(searcher)
    elif "--gui" in args:
        gui.main(searcher)
    else:
        print(__doc__)


def run():
    main(
        launchii.cli,
        launchii.gui,
        print,
        sys.argv,
        searcher(
            platform.system(),
            [
                "launchii.appsearch:StartMenuSearch",
                "launchii.macappsearch:OSXApplicationSearch",
            ],
        ),
    )
