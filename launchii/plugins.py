from typing import Any, List, Set, Tuple, Type
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
            map(build(True), filter(match, self.plugin_manager.get_active_plugins()))
        ) + list(
            map(build(False), filter(match, self.plugin_manager.get_inactive_plugins()))
        )


class ActivatePlugin(Action):
    def __init__(self, plugin_manager) -> None:
        self.plugin_manager = plugin_manager

    def can_do(self, result: SearchResult) -> bool:
        return result.uri().startswith("plugin:False")

    def do(self, result: PluginSearchResult) -> Any:
        self.plugin_manager.activate_plugin(result._plugin_string)

    def display(self) -> str:
        return "activate"


class DeactivatePlugin(Action):
    def __init__(self, plugin_manager) -> None:
        self.plugin_manager = plugin_manager

    def can_do(self, result: SearchResult) -> bool:
        return result.uri().startswith("plugin:True")

    def do(self, result: PluginSearchResult) -> Any:
        self.plugin_manager.deactivate_plugin(result._plugin_string)

    def display(self) -> str:
        return "deactivate"


class Index(LaunchiiPluginIndex):
    def searchers(self) -> List[Type[Searcher]]:
        return [PluginSearcher]

    def actions(self) -> List[Type[Action]]:
        return [ActivatePlugin, DeactivatePlugin]


class PluginManager:

    all_plugins = {
        "launchiicontrib.appsearch",
        "launchiicontrib.openaction",
        "launchii.plugins",
    }

    default_plugins = {
        "launchiicontrib.appsearch",
        "launchiicontrib.openaction",
        "launchii.plugins",
    }

    always_plugins = {"launchii.plugins"}

    def __init__(self, user_config_dir, bootstrap_provider_spec) -> None:
        me = self

        class SelfBindingSpec(pinject.BindingSpec):
            def provide_plugin_manager(self):
                return me

        self.user_config_dir = user_config_dir
        self._specs = [bootstrap_provider_spec, SelfBindingSpec()]
        self.active_plugins: Set[str] = set()

    def get_active_searchers(self) -> List[Searcher]:
        plugin_list = self._read_plugin_file()
        (searchers, _) = self._instantiate_plugins(plugin_list)
        return searchers

    def get_active_actions(self) -> List[Action]:
        plugin_list = self._read_plugin_file()
        (_, actions) = self._instantiate_plugins(plugin_list)
        return actions

    def deactivate_plugin(self, plugin_string):
        self.active_plugins.remove(plugin_string)
        self._write_plugin_file()

    def activate_plugin(self, plugin_string) -> Set[str]:
        self.active_plugins.add(plugin_string)
        self._write_plugin_file()
        return self.active_plugins

    def get_active_plugins(self):
        return self.active_plugins

    def get_inactive_plugins(self):
        return self.all_plugins - self.active_plugins

    def _read_plugin_file(self) -> Set[str]:
        try:
            with open(self.user_config_dir / "plugins.json") as f:
                from_file = set(json.load(f))
                self.active_plugins = from_file & self.all_plugins | self.always_plugins
        except FileNotFoundError as err:
            self.active_plugins = self.default_plugins
            self._write_plugin_file()
        return self.active_plugins

    def _write_plugin_file(self):
        self.user_config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.user_config_dir / "plugins.json", "w") as f:
            json.dump(list(self.active_plugins), f)

    def _instantiate_plugins(
        self,
        packages: Set[str],
    ) -> Tuple[List[Searcher], List[Action]]:

        searchers: List[Searcher] = []
        actions: List[Action] = []

        modules = list(map(importlib.import_module, packages))
        instantiator = pinject.new_object_graph(
            modules=modules + [sys.modules[__name__]],
            binding_specs=self._specs,
        )

        for module in modules:
            index_class = getattr(module, "Index")
            index = instantiator.provide(index_class)
            searchers.extend(map(instantiator.provide, index.searchers()))
            actions.extend(map(instantiator.provide, index.actions()))

        return (searchers, actions)
