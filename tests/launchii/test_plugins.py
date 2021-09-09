import json

import pytest
import pinject

import launchiicontrib.appsearch.appsearch as appsearch
import launchiicontrib.openaction.openaction as openaction
from launchii.plugins import PluginManager


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