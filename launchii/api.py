"""launchii plugin API

By implementing one of the below protocols and then adding
the coordinates to the object to the launchii main method
a plugin developer can add arbitrary search capabilities.
"""

import typing as t


class Searcher(t.Protocol):
    @staticmethod
    def supported_environment(platform: str) -> bool:
        """Returns true if the searcher will run properly on this platform"""
        ...

    def search(self, search_term) -> dict:
        """Have this plugin search for a search term

        Returns a dictionary that maps search terms to values"""
        ...

    def get_path(self, term) -> str:
        """Have this plugin search for an exact term and return the value"""
        ...
