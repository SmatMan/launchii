from launchii.api import SearchResult
import pytest
from unittest.mock import Mock
import pinject
import json

from launchii.core import PluginLaunchii, PluginManager
import launchiicontrib.appsearch.appsearch as appsearch
import launchiicontrib.openaction.openaction as openaction


class MockSearchResult:
    def __init__(self, key) -> None:
        self._key = key

    def display(self) -> str:
        return self._key

    def uri(self) -> str:
        return "mock:" + self._key


class FakeProviderSpec(pinject.BindingSpec):
    def __init__(self, system) -> None:
        self.system = system

    def provide_app_dirs(self):
        return None

    def provide_user_config_dir(self, app_dirs):
        return None

    def provide_system(self):
        return self.system


@pytest.mark.parametrize(
    "system, expected_searchers, expected_actions",
    [
        ("Darwin", [appsearch.OSXApplicationSearch], [openaction.OSXOpen]),
        ("Windows", [appsearch.StartMenuSearch], [openaction.WindowsOpen]),
    ],
)
def test_plugins_load_when_platform(system, expected_searchers, expected_actions):

    (searchers, actions) = PluginManager(
        None, FakeProviderSpec(system)
    )._instantiate_plugins(
        [
            "launchiicontrib.appsearch",
            "launchiicontrib.openaction",
        ],
    )

    assert isinstance(searchers[0], expected_searchers[0])
    assert isinstance(actions[0], expected_actions[0])


def test_plugins_always_returning_defaults(tmp_path):
    plugin_file = open(tmp_path / "plugins.json", "w+")
    json.dump(["x", "y"], plugin_file)
    plugin_file.close()
    assert PluginManager(None, FakeProviderSpec("test"))._load_plugin_file(
        tmp_path, ["a", "b"]
    ) == ["a", "b"]


def test_plugins_default_if_file_not_found(tmp_path):
    assert PluginManager(None, FakeProviderSpec("test"))._load_plugin_file(
        tmp_path, ["a", "b"]
    ) == ["a", "b"]


def test_plugins_create_default_files_if_not_found(tmp_path):
    assert PluginManager(None, FakeProviderSpec("test"))._load_plugin_file(
        tmp_path, ["a", "b"]
    ) == ["a", "b"]
    plugin_file = open(tmp_path / "plugins.json", "r")
    assert json.load(plugin_file) == ["a", "b"]
    plugin_file.close()


@pytest.fixture
def plugin_manager_context():
    (plugin_manager, action, searcher1, searcher2) = Mock(), Mock(), Mock(), Mock()
    search_result = [MockSearchResult("test")]
    search_result2 = [MockSearchResult("test2")]
    plugin_manager.get_active_searchers.return_value = [searcher1, searcher2]
    plugin_manager.get_active_actions.return_value = [action]
    searcher1.search.return_value = search_result
    searcher2.search.return_value = search_result2
    return (plugin_manager, search_result + search_result2, [action])


def test_plugin_launchii_searches(plugin_manager_context):
    (plugin_manager, search_result, [action]) = plugin_manager_context
    launchii = PluginLaunchii(plugin_manager)
    solutions = launchii.search("test search")
    assert solutions[0].item == search_result[0]
    assert solutions[0].action == action


def test_plugin_launchii_incorporates_all_search_results(plugin_manager_context):
    (plugin_manager, search_result, [action]) = plugin_manager_context
    launchii = PluginLaunchii(plugin_manager)
    solutions = launchii.search("test search")
    assert solutions[0].item == search_result[0]
    assert solutions[0].action == action
    assert solutions[1].item == search_result[1]
    assert solutions[1].action == action
