import pytest
from unittest.mock import Mock

from launchii.core import PluginLaunchii


class MockSearchResult:
    def __init__(self, key) -> None:
        self._key = key

    def display(self) -> str:
        return self._key

    def uri(self) -> str:
        return "mock:" + self._key


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
