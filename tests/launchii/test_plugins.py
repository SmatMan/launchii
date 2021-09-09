import json
from typing import Set

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


def test_plugins_default_if_file_not_found(tmp_path):
    assert (
        PluginManager(tmp_path, FakeProviderSpec("test"))._read_plugin_file()
        == PluginManager.default_plugins
    )


def test_plugins_create_default_files_if_not_found(tmp_path):
    PluginManager(tmp_path, FakeProviderSpec("test"))._read_plugin_file()
    plugin_file = open(tmp_path / "plugins.json", "r")
    assert set(json.load(plugin_file)) == PluginManager.default_plugins
    plugin_file.close()


def test_always_plugins_included_always(tmp_path):
    with open(tmp_path / "plugins.json", "w") as plugin_file:
        json.dump(["bad_plugin"], plugin_file)
    plugins = PluginManager(tmp_path, FakeProviderSpec("test"))._read_plugin_file()
    assert PluginManager.always_plugins & plugins == PluginManager.always_plugins


def test_plugins_not_in_all_plugins_removed(tmp_path):
    with open(tmp_path / "plugins.json", "w") as plugin_file:
        json.dump(["bad_plugin", "launchii.plugins"], plugin_file)
    plugins: Set[str] = PluginManager(
        tmp_path, FakeProviderSpec("test")
    )._read_plugin_file()
    assert plugins & PluginManager.all_plugins == plugins
