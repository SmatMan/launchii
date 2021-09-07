from typing import Any, List, Tuple
import pathlib
import json
import importlib

import pinject

from launchii.api import Action, Item, Searcher, Solution


class BasicSolution:
    def __init__(self, item: Item, action: Action) -> None:
        self.item = item
        self.action = action

    def describe(self) -> str:
        return str(self.item.name)

    def execute(self) -> Any:
        return self.action.do(self.item)


class PluginLaunchii:
    @staticmethod
    def _load_plugin_file(config_dir: pathlib.Path, default) -> List[str]:
        try:
            with open(config_dir / "plugins.json") as f:
                return default
        except FileNotFoundError as err:
            config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_dir / "plugins.json", "w") as f:
                json.dump(default, f)
            return default

    @staticmethod
    def _instantiate_plugins(
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

    def __init__(self, user_config_dir, bootstrap_provider_spec) -> None:
        self.user_config_dir = user_config_dir

        instantiator = pinject.new_object_graph(binding_specs=[bootstrap_provider_spec])

        plugin_list = PluginLaunchii._load_plugin_file(
            self.user_config_dir,
            ["launchiicontrib.appsearch", "launchiicontrib.openaction"],
        )

        (self.searchers, self.actions) = PluginLaunchii._instantiate_plugins(
            plugin_list, instantiator
        )

    def search(self, search_term: str) -> List[Solution]:
        return list(
            map(
                lambda i: BasicSolution(i, self.actions[0]),
                self.searchers[0].search(search_term),
            )
        )
