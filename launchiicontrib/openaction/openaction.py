import os
from typing import Any
from launchii.api import SearchResult


class WindowsOpen:
    def do(self, item: SearchResult) -> Any:
        return os.startfile(item.uri())

    def can_do(self, item: SearchResult) -> bool:
        return item.uri().startswith("file:")

    def display(self) -> str:
        return "open"


class OSXOpen:
    def do(self, item: SearchResult) -> Any:
        return os.system(f'open "{str(item.uri())}"')

    def can_do(self, item: SearchResult) -> bool:
        return item.uri().startswith("file:")

    def display(self) -> str:
        return "open"
