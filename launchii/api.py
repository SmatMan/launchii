"""launchii plugin API

Launchii plugins are created and published to PyPi independently
of Launchii itself. Launchii plugins should be published into PyPi following
PEP423 guidance for default community contributions. Which is documented here: https://www.python.org/dev/peps/pep-0423/#id101
In addition to naming the package correctly they should also implement a special
class named Index in the root __init__.py file of the package.

e.g.:
    I am creating a plugin for bookmarks, my package name in PyPi is 'launchiicontrib.bookmarks'
    and launchiicontrib.bookmarks.Index is a class in my package.

Your Index class, as well as any type objects it returns can be dependency injected
with launchii services.

e.g.:
    def __init__(self, system, user_config_dir)

In the above example system and user_config_dir are two of such
parameters of which there are more.  user_config_dir provides a
Pathlib.Path to launchii's configuration directory on disk, and
system provides a string defining the system launchii is running
inside, such as Windows or Darwin.  There are other parameters as
well. To understand more details about Index as well as the classes
it can return please read additional documentation below.

Launchii plugins should always match the major version number of launchii itself, the launchii major version
represents the API documented in this file, and whenever it changes, plugins will need to release new versions
"""

import pathlib
from typing import Any, List, Protocol, Type, Union
from dataclasses import dataclass

Location = Union[pathlib.Path, str]


@dataclass
class Item:
    name: str
    location: Location


class Searcher(Protocol):
    """To be written"""

    def search(self, search_term: str) -> List[Item]:
        """Have this plugin search for a search term

        Returns a list of search results"""
        ...


class Action(Protocol):
    """To be written"""

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


class LaunchiiPluginIndex(Protocol):
    """Represents a Launchii Plugin Index"""

    def searchers(self) -> List[Type[Searcher]]:
        ...

    def actions(self) -> List[Type[Action]]:
        ...
