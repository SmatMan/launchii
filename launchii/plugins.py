from typing import Any, List, Tuple, Type
import pathlib
import json
import importlib
import sys

import pinject

from launchii.api import Action, LaunchiiPluginIndex, SearchResult, Searcher


class PluginSearchResult(SearchResult):
    def __init__(self, plugin_string: str, active: bool) -> None:
        self._plugin_string = plugin_string
        self._active = active

    def display(self) -> str:
        return self._plugin_string

    def uri(self) -> str:
        return f"plugin:{self._active}:{self._plugin_string}"


class PluginSearcher(Searcher):
    def __init__(self, plugin_manager) -> None:
        self.plugin_manager = plugin_manager

    def search(self, search_term: str) -> List[SearchResult]:

        match = (
            lambda plugin: search_term.lower() in plugin.lower()
            and plugin != "launchii.core"
        )
        build = lambda active: lambda plugin: PluginSearchResult(plugin, active)

        return list(
            map(build(True), filter(match, self.plugin_manager.active_plugins))
        ) + list(map(build(False), filter(match, self.plugin_manager.inactive_plugins)))


class ActivatePlugin(Action):
    def __init__(self, plugin_manager) -> None:
        self.plugin_manager = plugin_manager

    def can_do(self, result: SearchResult) -> bool:
        return result.uri().startswith("plugin:False")

    def do(self, result: SearchResult) -> Any:
        print(f"To implement: activate plugin {result.display()}")

    def display(self) -> str:
        return "activate"


class DeactivatePlugin(Action):
    def __init__(self, plugin_manager) -> None:
        self.plugin_manager = plugin_manager

    def can_do(self, result: SearchResult) -> bool:
        return result.uri().startswith("plugin:True")

    def do(self, result: SearchResult) -> Any:
        print(f"To implement: deactivate plugin {result.display()}")

    def display(self) -> str:
        return "deactivate"


class Index(LaunchiiPluginIndex):
    def searchers(self) -> List[Type[Searcher]]:
        return [PluginSearcher]

    def actions(self) -> List[Type[Action]]:
        return [ActivatePlugin, DeactivatePlugin]


class PluginManager:
    def __init__(self, user_config_dir, bootstrap_provider_spec) -> None:
        self.user_config_dir = user_config_dir
        self.boostrap_provider_spec = bootstrap_provider_spec
        self.active_plugins = [
            "launchiicontrib.appsearch",
            "launchiicontrib.openaction",
            "launchii.plugins",
        ]
        self.inactive_plugins: List[str] = []

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
            self.active_plugins,
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
