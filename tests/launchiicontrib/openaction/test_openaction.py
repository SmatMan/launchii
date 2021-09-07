import launchiicontrib.openaction.openaction as openaction
import pytest
from unittest.mock import Mock


from launchiicontrib.openaction.openaction import OSXOpen, WindowsOpen


def test_osx_can_open_files():
    action = OSXOpen()
    test_result = Mock()
    test_result.uri.return_value = "file://something"
    assert action.can_do(test_result) is True


def test_windows_can_open_files():
    action = WindowsOpen()
    test_result = Mock()
    test_result.uri.return_value = "file://something"
    assert action.can_do(test_result) is True


def test_windows_verb():
    assert WindowsOpen().display() == "open"


def test_osx_verb():
    assert OSXOpen().display() == "open"
