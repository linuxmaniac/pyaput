from . import invoke


def test_version(
    cli,
):
    result = invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "pyaput -" in result.output
