from . import invoke


def test_help():
    result = invoke(["--help"])
    assert result.exit_code == 0
    assert "files" in result.output
