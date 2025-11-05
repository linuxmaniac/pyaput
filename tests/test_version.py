from . import invoke


def test_version():
    result = invoke(["version"])
    assert result.exit_code == 0
    assert "pyaput -" in result.output
