from launchii.api import Action, Searcher
from typing import List, Type

from launchiicontrib.openaction.openaction import OSXOpen, WindowsOpen


class Index:
    def __init__(self, system) -> None:
        self.system = system

    def searchers(self) -> List[Type[Searcher]]:
        return []

    def actions(self) -> List[Type[Action]]:
        if self.system == "Darwin":
            return [OSXOpen]
        elif self.system == "Windows":
            return [WindowsOpen]
        else:
            return []
