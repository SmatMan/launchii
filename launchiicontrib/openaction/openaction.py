import os
from typing import Any
from launchii.api import Item


class WindowsOpen:
    def do(self, item: Item) -> Any:
        return os.startfile(item.location)


class OSXOpen:
    def do(self, item: Item) -> Any:
        return os.system(f'open "{str(item.location)}"')
