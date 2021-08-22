import pathlib
import functools
from typing import Callable, List

from launchii.api import Result


class FileSearch:

    roots: List[pathlib.Path] = []
    globs: List[str] = []
    predicates: List[Callable[[pathlib.Path], bool]] = []

    def result_builder(self, file) -> Result:
        return Result(file.name.lower(), file)

    def search(self, search_term: str) -> List[Result]:
        return list(
            filter(
                lambda r: search_term in str(r.location).lower(),
                self._search_for_apps(),
            )
        )

    @functools.cache
    def _search_for_apps(self) -> List[Result]:

        rawFileList = []
        for root in self.roots:
            for glob in self.globs:
                for file in root.glob(glob):
                    if all(map(lambda p: p(file), self.predicates)):
                        rawFileList.append(self.result_builder(file))

        return sorted(rawFileList, key=lambda r: r.name)


class StartMenuSearch(FileSearch):

    roots = [
        pathlib.Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs"),
        pathlib.Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu",
    ]

    globs = ["**/*.lnk"]

    predicates = [lambda path: not path.name.startswith("desktop")]

    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Windows"


class OSXApplicationSearch(FileSearch):

    roots = [
        pathlib.Path("/Applications"),
        pathlib.Path("/System/Applications"),
        pathlib.Path.home() / "Applications",
    ]

    globs = ["*.app"]

    def result_builder(self, file) -> Result:
        return Result(file.stem, file)

    @staticmethod
    def supported_environment(platform: str) -> bool:
        return platform == "Darwin"

    def getIcon(self, path: pathlib.Path) -> pathlib.Path:
        for i in path.glob(f"Contents/Resources/*.icns"):
            icon = i
        return icon
