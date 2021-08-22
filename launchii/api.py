"""launchii plugin API

By implementing one of the below protocols and then adding
the coordinates to the object to the launchii main method
a plugin developer can add arbitrary search capabilities.
"""

import pathlib
from typing import Any, List, Protocol, Union, runtime_checkable
from dataclasses import dataclass

Location = Union[pathlib.Path, str]


@dataclass
class Item:
    name: str
    location: Location


class Plugin(Protocol):
    @staticmethod
    def supported_environment(platform: str) -> bool:
        """Returns true if the searcher will run properly on this platform"""
        ...


@runtime_checkable
class Searcher(Protocol):
    def search(self, search_term: str) -> List[Item]:
        """Have this plugin search for a search term

        Returns a list of search results"""
        ...


@runtime_checkable
class Action(Protocol):
    def do(self, result: Item) -> Any:
        """Preliminay interface for actions"""
        ...
