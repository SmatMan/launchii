import unittest.mock as mock
import pytest
import json

import launchii.appsearch as appsearch
import launchii.macappsearch as macappsearch
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
def searcher():
    return mock.Mock()


def test_default_behavior_prints_documentation(cli, gui, print_function, searcher):
    args = []
    launchii.main(cli, gui, print_function, args, searcher)
    print_function.assert_called_once_with(launchii.__doc__)


def test_gui_triggered_with_parameter(cli, gui, print_function, searcher):
    args = ["--gui"]
    launchii.main(cli, gui, print_function, args, searcher)
    gui.main.assert_called_once()


def test_cli_triggered_with_parameter(cli, gui, print_function, searcher):
    args = ["--cli"]
    launchii.main(cli, gui, print_function, args, searcher)
    cli.main.assert_called_once()


@pytest.mark.parametrize(
    "platform, expected",
    [
        ("Darwin", macappsearch.OSXApplicationSearch),
        ("Windows", appsearch.StartMenuSearch),
    ],
)
def test_searcher_selected_when_platform(platform, expected):
    searcher = launchii.searcher(
        platform,
        [
            "launchii.appsearch:StartMenuSearch",
            "launchii.macappsearch:OSXApplicationSearch",
        ],
    )
    assert isinstance(searcher, expected)


def test_plugins_loaded_from_file(tmp_path):
    plugin_file = open(tmp_path / "plugins.json", "w+")
    json.dump(["x", "y"], plugin_file)
    plugin_file.close()
    assert launchii.load_plugins(tmp_path, ["a", "b"]) == ["x", "y"]


def test_plugins_default_if_file_not_found(tmp_path):
    assert launchii.load_plugins(tmp_path, ["a", "b"]) == ["a", "b"]


def test_plugins_create_default_files_if_not_found(tmp_path):
    assert launchii.load_plugins(tmp_path, ["a", "b"]) == ["a", "b"]
    plugin_file = open(tmp_path / "plugins.json", "r")
    assert json.load(plugin_file) == ["a", "b"]
    plugin_file.close()
