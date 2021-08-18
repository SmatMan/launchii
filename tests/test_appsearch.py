import launchii.appsearch as app


def test_active_on_windows():
    assert True == app.StartMenuSearch.supported_environment("Windows")


def test_not_active_elsewhere():
    assert False == app.StartMenuSearch.supported_environment("Elsewhere")
