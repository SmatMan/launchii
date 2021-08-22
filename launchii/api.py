"""launchii plugin API

By implementing one of the below protocols and then adding
the coordinates to the object to the launchii main method
a plugin developer can add arbitrary search capabilities.
"""

import pathlib
from typing import List, Protocol, Union
from dataclasses import dataclass

Location = Union[pathlib.Path, str]


@dataclass
class Result:
    name: str
    location: Location


class Searcher(Protocol):
    @staticmethod
    def supported_environment(platform: str) -> bool:
        """Returns true if the searcher will run properly on this platform"""
        ...

    def search(self, search_term) -> List[Result]:
        """Have this plugin search for a search term

        Returns a list of search results"""
        ...
