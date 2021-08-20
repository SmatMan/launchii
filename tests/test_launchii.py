import unittest.mock as mock
import pytest

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
