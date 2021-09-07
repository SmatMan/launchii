import pathlib
import functools
from typing import Callable, List

from launchii.api import SearchResult


class FileSearchResult:
    def __init__(self, file: pathlib.Path) -> None:
        self._file = file

    def display(self) -> str:
        return self._file.stem

    def uri(self) -> str:
        return self._file.as_uri()


class FileSearch:

    roots: List[pathlib.Path] = []
    globs: List[str] = []
    predicates: List[Callable[[pathlib.Path], bool]] = []

    def search(self, search_term: str) -> List[SearchResult]:
        return list(
            filter(
                lambda r: search_term.lower() in r.display().lower(),
                self._search_for_apps(),
            )
        )

    @functools.cache
    def _search_for_apps(self) -> List[SearchResult]:

        rawFileList = []
        for root in self.roots:
            for glob in self.globs:
                for file in root.glob(glob):
                    if all(map(lambda p: p(file), self.predicates)):
                        rawFileList.append(FileSearchResult(file))

        return sorted(rawFileList, key=lambda r: r.display())


class StartMenuSearch(FileSearch):

    roots = [
        pathlib.Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs"),
        pathlib.Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu",
    ]

    globs = ["**/*.lnk"]

    predicates = [lambda path: not path.name.startswith("desktop")]


class OSXApplicationSearch(FileSearch):

    roots = [
        pathlib.Path("/Applications"),
        pathlib.Path("/System/Applications"),
        pathlib.Path.home() / "Applications",
    ]

    globs = ["*.app"]

    def getIcon(self, path: pathlib.Path) -> pathlib.Path:
        for i in path.glob(f"Contents/Resources/*.icns"):
            icon = i
        return icon
