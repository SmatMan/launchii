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
    """Plugins for launchii

    Plugins for launchii, in addition to requiring the
    supported_environment static method and to implement a
    plugin protocol that actually does something such as
    Action or Searcher may also implement a constructor that can
    accept one or more launchii services via its parameters

    e.g.:
        def __init__(self, system, user_config_dir)

    In the above example system and user_config_dir are two of such
    parameters of which there are more.  user_config_dir provides a
    Pathlib.Path to launchii's configuration directory on disk, and
    system provides a string defining the system launchii is running
    inside, such as Windows or Darwin.  There are other parameters as
    well.

    """

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


class UserInterface(Protocol):
    def start(self):
        ...


class Solution(Protocol):
    def describe(self) -> str:
        ...

    def execute(self) -> Any:
        ...


class Launchii(Protocol):
    def search(self, search_term: str) -> List[Solution]:
        ...
