import launchii.openaction as openaction
import pytest


@pytest.mark.parametrize(
    "platform, clazz_, expected",
    [
        ("Darwin", openaction.OSXOpen, True),
        ("Windows", openaction.OSXOpen, False),
        ("Darwin", openaction.WindowsOpen, False),
        ("Windows", openaction.WindowsOpen, True),
    ],
)
def test_environment_support(platform, clazz_, expected):
    assert expected == clazz_.supported_environment(platform)
