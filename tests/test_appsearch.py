from launchii.api import Item
import launchii.appsearch as app
import pathlib

import pytest


def setup_files(root_path, paths):
    for p in paths:
        path = pathlib.Path(root_path) / p
        path.parents[0].mkdir(parents=True, exist_ok=True)
        path.touch()


def assert_results(expected, actual):
    names = list(map(lambda item: item.name, actual))
    for name in names:
        assert name in expected
    assert len(names) == len(expected)


@pytest.fixture
def start_menu_search(tmp_path):
    searcher = app.StartMenuSearch()
    searcher.roots = [tmp_path]
    return searcher


def test_active_on_windows():
    assert True == app.StartMenuSearch.supported_environment("Windows")


def test_not_active_elsewhere():
    assert False == app.StartMenuSearch.supported_environment("Elsewhere")


def test_includes_lnk_files(tmp_path, start_menu_search):
    setup_files(tmp_path, ["testing.lnk"])
    result = start_menu_search.search("test")
    assert_results(["testing.lnk"], result)


def test_excludes_files_beginning_with_desktop(tmp_path, start_menu_search):
    setup_files(tmp_path, ["desktop_file.lnk", "testing.lnk"])
    result = start_menu_search.search("test")
    assert_results(["testing.lnk"], result)


def test_searches_child_directories(tmp_path, start_menu_search):
    setup_files(
        tmp_path, ["desktop_file.lnk", "testing.lnk", "child/another-test-file.lnk"]
    )
    result = start_menu_search.search("test")
    assert_results(["testing.lnk", "another-test-file.lnk"], result)


def test_results_sorted_by_name(tmp_path, start_menu_search):
    setup_files(tmp_path, ["filec.lnk", "filea.lnk", "fileb.lnk"])
    result = start_menu_search.search("file")
    assert True == all(
        map(
            lambda i: i[0].name == i[1],
            (zip(result, ["filea.lnk", "fileb.lnk", "filec.lnk"])),
        )
    )


def test_integration_test(tmp_path, start_menu_search):
    setup_files(
        tmp_path,
        [
            "desktop_file.lnk",
            "testing.lnk",
            "child/another-test-file.lnk",
            "child/desktop_file2.lnk",
            "child/child2/file4.lnk",
            "desktop/link3.lnk",
            "not_a_link.txt",
        ],
    )
    result = start_menu_search.search("test")
    assert_results(
        ["testing.lnk", "another-test-file.lnk", "link3.lnk", "file4.lnk"], result
    )


@pytest.fixture
def osx_search(tmp_path):
    searcher = app.OSXApplicationSearch()
    searcher.roots = [tmp_path]
    return searcher


def test_active_on_darwin():
    assert True == app.OSXApplicationSearch.supported_environment("Darwin")


def test_not_active_not_on_darwin():
    assert False == app.OSXApplicationSearch.supported_environment("Elsewhere")


def test_darwin_applications(tmp_path, osx_search):
    setup_files(
        tmp_path,
        [
            "Fortune.app/desktop_file.lnk",
            "testing.lnk",
            "not_a_link.txt",
            "Fortune2.app/",
            "Fortune3.app/something",
        ],
    )
    result = osx_search.search("fortune")
    assert_results(["Fortune", "Fortune2", "Fortune3"], result)
