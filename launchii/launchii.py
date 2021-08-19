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

Loader = t.Callable[[str], object]


def get_searcher_class(module_name: str, import_module: Loader) -> t.Type[BaseSearch]:
    pieces = module_name.split(":")
    actual_module = import_module(pieces[0])
    return getattr(actual_module, pieces[1])


def searcher(system: str, import_module: Loader, packages: t.List[str]) -> BaseSearch:
    for package in packages:
        searcher_class = get_searcher_class(package, import_module)
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
            importlib.import_module,
            [
                "launchii.appsearch:StartMenuSearch",
                "launchii.macappsearch:OSXApplicationSearch",
            ],
        ),
    )
