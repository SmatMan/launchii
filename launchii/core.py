from typing import Any, List, Tuple
import pathlib
import json
import importlib
import sys
import itertools

import pinject

from launchii.api import Action, SearchResult, Searcher, Solution


class BasicSolution:
    def __init__(self, item: SearchResult, action: Action) -> None:
        self.item = item
        self.action = action

    def describe(self) -> str:
        return str(self.item.display())

    def execute(self) -> Any:
        return self.action.do(self.item)


class PluginManager:
    def __init__(self, user_config_dir, bootstrap_provider_spec) -> None:
        self.user_config_dir = user_config_dir
        self.boostrap_provider_spec = bootstrap_provider_spec

    def get_active_searchers(self) -> List[Searcher]:
        plugin_list = self._get_plugin_list_from_config()
        (searchers, _) = self._instantiate_plugins(plugin_list)
        return searchers

    def get_active_actions(self) -> List[Action]:
        plugin_list = self._get_plugin_list_from_config()
        (_, actions) = self._instantiate_plugins(plugin_list)
        return actions

    def _get_plugin_list_from_config(self):
        return self._load_plugin_file(
            self.user_config_dir,
            ["launchiicontrib.appsearch", "launchiicontrib.openaction"],
        )

    def _load_plugin_file(self, config_dir: pathlib.Path, default) -> List[str]:
        try:
            with open(config_dir / "plugins.json") as f:
                return default
        except FileNotFoundError as err:
            config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_dir / "plugins.json", "w") as f:
                json.dump(default, f)
            return default

    def _instantiate_plugins(
        self,
        packages: List[str],
    ) -> Tuple[List[Searcher], List[Action]]:

        searchers: List[Searcher] = []
        actions: List[Action] = []

        modules = list(map(importlib.import_module, packages))
        instantiator = pinject.new_object_graph(
            modules=modules + [sys.modules[__name__]],
            binding_specs=[self.boostrap_provider_spec],
        )

        for module in modules:
            index_class = getattr(module, "Index")
            index = instantiator.provide(index_class)
            searchers.extend(map(instantiator.provide, index.searchers()))
            actions.extend(map(instantiator.provide, index.actions()))

        return (searchers, actions)


class PluginLaunchii:
    def __init__(self, plugin_manager: PluginManager) -> None:
        self.plugin_manager = plugin_manager

    def search(self, search_term: str) -> List[Solution]:
        searchers = self.plugin_manager.get_active_searchers()
        action = self.plugin_manager.get_active_actions()[0]

        return list(
            map(
                lambda item: BasicSolution(item, action),
                itertools.chain.from_iterable(
                    map(lambda searcher: searcher.search(search_term), searchers)
                ),
            )
        )
