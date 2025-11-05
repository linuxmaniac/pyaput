from . import invoke


def test_config():
    result = invoke(["config"])
    assert result.exit_code == 0
    assert "aptly_api_url=" in result.output
