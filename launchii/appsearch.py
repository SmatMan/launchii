import os
from collections import OrderedDict
import getpass
import json


class StartMenuSearch:
    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Windows"

    def __init__(self):
        with open("index.json", "r") as f:  # load index
            self.index = json.load(f)

    def search(self, search_term) -> dict:
        results = {}
        for i in self.index:  # iterate over index
            if search_term in self.index[i].lower():  # if search term is in index
                # append i to results as key and index[i] as value
                results[i] = self.index[i]
        return results

    def get_path(self, term) -> str:
        path = self.index[term]
        return path

    def createindex(
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
                    print(file)
                    if file.endswith(".lnk") and not file.startswith("desktop"):
                        rawFileList[file.lower()] = os.path.join(root, file)

        filelist = OrderedDict(sorted(rawFileList.items(), key=lambda t: t[0]))

        return filelist

    def saveIndex(self, output="index.json"):
        index = self.createindex()
        with open(output, "w") as f:
            f.write(json.dumps(index, indent=4))
