import unittest.mock as mock
import pytest

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
