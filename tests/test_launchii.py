import unittest.mock as mock
import pytest
import json

import launchii.appsearch as appsearch
import launchii.openaction as openaction
import launchii.launchii as launchii


@pytest.fixture
def cli():
    return mock.Mock()


@pytest.fixture
def gui():
    return mock.Mock()


@pytest.fixture
def print_function():
    return mock.Mock()


@pytest.fixture
def launchiiApp():
    return mock.Mock()


def test_default_behavior_prints_documentation(cli, gui, print_function, launchiiApp):
    args = []
    launchii.main(cli, gui, print_function, args, launchiiApp)
    print_function.assert_called_once_with(launchii.__doc__)


def test_gui_triggered_with_parameter(cli, gui, print_function, launchiiApp):
    args = ["--gui"]
    launchii.main(cli, gui, print_function, args, launchiiApp)
    gui.assert_called_once()


def test_cli_triggered_with_parameter(cli, gui, print_function, launchiiApp):
    args = ["--cli"]
    launchii.main(cli, gui, print_function, args, launchiiApp)
    cli.assert_called_once()


@pytest.mark.parametrize(
    "platform, expected_searchers, expected_actions",
    [
        ("Darwin", [appsearch.OSXApplicationSearch], [openaction.OSXOpen]),
        ("Windows", [appsearch.StartMenuSearch], [openaction.WindowsOpen]),
    ],
)
def test_plugins_load_when_platform(platform, expected_searchers, expected_actions):
    class MockInstantiator(object):
        pass

    instantiator = MockInstantiator()
    instantiator.provide = lambda x: x()

    (searchers, actions) = launchii.instantiate_plugins(
        platform,
        [
            "launchii.appsearch:StartMenuSearch",
            "launchii.appsearch:OSXApplicationSearch",
            "launchii.openaction:WindowsOpen",
            "launchii.openaction:OSXOpen",
        ],
        instantiator,
    )

    assert isinstance(searchers[0], expected_searchers[0])
    assert isinstance(actions[0], expected_actions[0])


def test_plugins_always_returning_defaults(tmp_path):
    plugin_file = open(tmp_path / "plugins.json", "w+")
    json.dump(["x", "y"], plugin_file)
    plugin_file.close()
    assert launchii.load_plugin_file(tmp_path, ["a", "b"]) == ["a", "b"]


def test_plugins_default_if_file_not_found(tmp_path):
    assert launchii.load_plugin_file(tmp_path, ["a", "b"]) == ["a", "b"]


def test_plugins_create_default_files_if_not_found(tmp_path):
    assert launchii.load_plugin_file(tmp_path, ["a", "b"]) == ["a", "b"]
    plugin_file = open(tmp_path / "plugins.json", "r")
    assert json.load(plugin_file) == ["a", "b"]
    plugin_file.close()
