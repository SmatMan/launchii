"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
import sys
import platform
import importlib
import pathlib
import json
from typing import Any, List, Tuple

import pinject
import appdirs

from launchii.api import Action, Item, Searcher, Solution
import launchii.cli
import launchii.gui

_default_plugins = ["launchiicontrib.appsearch", "launchiicontrib.openaction"]


class BasicSolution:
    def __init__(self, item: Item, action: Action) -> None:
        self.item = item
        self.action = action

    def describe(self) -> str:
        return str(self.item.name)

    def execute(self) -> Any:
        return self.action.do(self.item)


class BasicLaunchii:
    def __init__(self, seacher: Searcher, action: Action) -> None:
        self.searcher = seacher
        self.action = action

    def search(self, search_term: str) -> List[Solution]:
        return list(
            map(
                lambda i: BasicSolution(i, self.action),
                self.searcher.search(search_term),
            )
        )


def load_plugin_file(config_dir: pathlib.Path, default) -> List[str]:
    try:
        with open(config_dir / "plugins.json") as f:
            return default
    except FileNotFoundError as err:
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_dir / "plugins.json", "w") as f:
            json.dump(default, f)
        return default


def instantiate_plugins(
    packages: List[str],
    instantiator,
) -> Tuple[List[Searcher], List[Action]]:

    searchers: List[Searcher] = []
    actions: List[Action] = []

    for package in packages:
        actual_module = importlib.import_module(package)
        index_class = getattr(actual_module, "Index")
        index = instantiator.provide(index_class)
        searchers.extend(map(instantiator.provide, index.searchers()))
        actions.extend(map(instantiator.provide, index.actions()))

    return (searchers, actions)


def main(cli, gui, print, args, launchii):
    if "--cli" in args:
        cli(launchii).start()
    elif "--gui" in args:
        gui(launchii).start()
    else:
        print(__doc__)


def run():
    class BaseProviderSpec(pinject.BindingSpec):
        def provide_app_dirs(self):
            return appdirs.AppDirs("launchii")

        def provide_user_config_dir(self, app_dirs):
            return pathlib.Path(app_dirs.user_config_dir)

        def provide_system(self):
            return platform.system()

    instantiator = pinject.new_object_graph(binding_specs=[BaseProviderSpec()])

    dirs = appdirs.AppDirs("launchii")
    plugin_list = load_plugin_file(pathlib.Path(dirs.user_config_dir), _default_plugins)

    (searchers, actions) = instantiate_plugins(plugin_list, instantiator)

    launchiiApp = BasicLaunchii(searchers[0], actions[0])

    main(launchii.cli.Cli, launchii.gui.Gui, print, sys.argv, launchiiApp)
