import os
from typing import Any
from launchii.api import SearchResult


class WindowsOpen:
    def do(self, item: SearchResult) -> Any:
        return os.startfile(item.uri())


class OSXOpen:
    def do(self, item: SearchResult) -> Any:
        return os.system(f'open "{str(item.uri())}"')
