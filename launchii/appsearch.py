import os
from collections import OrderedDict
import getpass
import functools


class StartMenuSearch:
    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Windows"

    def search(self, search_term) -> dict:
        index = self._search_for_shortcuts()
        results = {}
        for i in index:  # iterate over index
            if search_term in index[i].lower():  # if search term is in index
                # append i to results as key and index[i] as value
                results[i] = index[i]
        return results

    @functools.cache
    def _search_for_shortcuts(
        self,
        path=[
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
            rf"C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu",
        ],
    ):
        rawFileList = {}

        for i in path:
            for root, dirs, files in os.walk(i, followlinks=False):
                for file in files:
                    if file.endswith(".lnk") and not file.startswith("desktop"):
                        rawFileList[file.lower()] = os.path.join(root, file)

        filelist = OrderedDict(sorted(rawFileList.items(), key=lambda t: t[0]))

        return filelist
