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

from launchii.api import Action, Searcher
import launchii.cli
import launchii.gui

_default_plugins = [
    "launchii.appsearch:StartMenuSearch",
    "launchii.appsearch:OSXApplicationSearch",
    "launchii.openaction:WindowsOpen",
    "launchii.openaction:OSXOpen",
]


def load_plugin_file(config_dir: pathlib.Path, default) -> t.List[str]:
    try:
        with open(config_dir / "plugins.json") as f:
            return default
    except FileNotFoundError as err:
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_dir / "plugins.json", "w") as f:
            json.dump(default, f)
        return default


def instantiate_plugins(
    system: str, packages: t.List[str]
) -> t.Tuple[t.List[Searcher], t.List[Action]]:

    searchers: t.List[Searcher] = []
    actions: t.List[Action] = []

    for package in packages:
        pieces = package.split(":")
        actual_module = importlib.import_module(pieces[0])
        class_ = getattr(actual_module, pieces[1])
        if class_.supported_environment(system):
            instance = class_()
            if isinstance(instance, Searcher):
                searchers.append(instance)
            elif isinstance(instance, Action):
                actions.append(instance)

    return (searchers, actions)


def main(cli, gui, print, args, searcher, runner):
    if "--cli" in args:
        cli.main(searcher, runner)
    elif "--gui" in args:
        gui.main(searcher, runner)
    else:
        print(__doc__)


def run():
    dirs = appdirs.AppDirs("launchii")
    plugin_list = load_plugin_file(pathlib.Path(dirs.user_config_dir), _default_plugins)

    (searchers, actions) = instantiate_plugins(platform.system(), plugin_list)

    main(launchii.cli, launchii.gui, print, sys.argv, searchers[0], actions[0])
