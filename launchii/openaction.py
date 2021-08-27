import os
from typing import Any
from launchii.api import Item


class WindowsOpen:
    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Windows"

    def do(self, item: Item) -> Any:
        return os.startfile(item.location)


class OSXOpen:
    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Darwin"

    def do(self, item: Item) -> Any:
        return os.system(f'open "{str(item.location)}"')
