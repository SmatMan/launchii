import os
from collections import OrderedDict
import getpass
import json
from launchii.crosssearch import BaseSearch


class StartMenuSearch(BaseSearch):
    
    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Windows"

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
