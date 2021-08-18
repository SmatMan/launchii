import launchii.macappsearch as app


def test_active_on_darwin():
    assert True == app.OSXApplicationSearch.supported_environment("Darwin")


def test_not_active_elsewhere():
    assert False == app.OSXApplicationSearch.supported_environment("Elsewhere")
