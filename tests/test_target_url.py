from tideway.main import Appliance


def test_bare_target_defaults_to_https():
    tw = Appliance("appliance.example", "token", api_version="1.14")

    assert tw.target_url == "https://appliance.example"
    assert tw.api == "https://appliance.example/api"
    assert tw.url == "https://appliance.example/api/v1.14"


def test_explicit_https_target_is_respected():
    tw = Appliance("https://appliance.example/base/", "token", api_version="1.14")

    assert tw.target_url == "https://appliance.example/base"
    assert tw.api == "https://appliance.example/base/api"
    assert tw.url == "https://appliance.example/base/api/v1.14"


def test_explicit_http_target_is_respected_for_prism():
    tw = Appliance("http://127.0.0.1:4010", "token", api_version="1.14")

    assert tw.target_url == "http://127.0.0.1:4010"
    assert tw.api == "http://127.0.0.1:4010/api"
    assert tw.url == "http://127.0.0.1:4010/api/v1.14"
