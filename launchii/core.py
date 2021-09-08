from typing import Any, List
import itertools

from launchii.api import Action, SearchResult, Solution
from launchii.plugins import PluginManager


class BasicSolution:
    def __init__(self, item: SearchResult, action: Action) -> None:
        self.item = item
        self.action = action

    def describe(self) -> str:
        return self.action.display() + " " + self.item.display()

    def execute(self) -> Any:
        return self.action.do(self.item)


class PluginLaunchii:
    def __init__(self, plugin_manager: PluginManager) -> None:
        self.plugin_manager = plugin_manager

    def search(self, search_term: str) -> List[Solution]:
        searchers = self.plugin_manager.get_active_searchers()
        actions = self.plugin_manager.get_active_actions()

        search_results = list(
            itertools.chain.from_iterable(
                map(lambda searcher: searcher.search(search_term), searchers)
            )
        )

        return list(
            map(
                lambda combo: BasicSolution(*combo),
                filter(
                    lambda combo: combo[1].can_do(combo[0]),
                    itertools.product(search_results, actions),
                ),
            )
        )
