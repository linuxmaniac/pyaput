from . import invoke


def test_help(cli):
    result = invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "files" in result.output
