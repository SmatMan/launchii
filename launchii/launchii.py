"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
import sys
import platform
import importlib
import typing as t
import pathlib
import json

import appdirs

from launchii.api import Searcher
import launchii.cli
import launchii.gui

_default_plugins = [
    "launchii.appsearch:StartMenuSearch",
    "launchii.macappsearch:OSXApplicationSearch",
]


def load_plugins(config_dir: pathlib.Path, default) -> t.List[str]:
    try:
        with open(config_dir / "plugins.json") as f:
            return json.load(f)
    except FileNotFoundError as err:
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_dir / "plugins.json", "w") as f:
            json.dump(default, f)
        return default


def get_searcher_class(module_name: str) -> t.Type[Searcher]:
    pieces = module_name.split(":")
    actual_module = importlib.import_module(pieces[0])
    return getattr(actual_module, pieces[1])


def searcher(system: str, packages: t.List[str]) -> Searcher:
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
    dirs = appdirs.AppDirs("launchii")

    main(
        launchii.cli,
        launchii.gui,
        print,
        sys.argv,
        searcher(
            platform.system(),
            load_plugins(pathlib.Path(dirs.user_config_dir), _default_plugins),
        ),
    )
