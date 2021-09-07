from typing import List, Type
from launchii.api import Action, Searcher
from launchiicontrib.appsearch.appsearch import StartMenuSearch, OSXApplicationSearch


class Index:
    def __init__(self, system) -> None:
        self.system = system

    def searchers(self) -> List[Type[Searcher]]:
        if self.system == "Darwin":
            return [OSXApplicationSearch]
        elif self.system == "Windows":
            return [StartMenuSearch]
        else:
            return []

    def actions(self) -> List[Type[Action]]:
        return []
