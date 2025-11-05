from . import invoke


def test_config(cli):
    result = invoke(cli, ["config"])
    assert result.exit_code == 0
    assert "aptly_api_url=" in result.output
