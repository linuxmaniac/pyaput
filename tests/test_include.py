from pathlib import Path
from . import invoke

FIXTURES = Path(__file__).resolve(strict=True).parent / "fixtures"


def test_include_help(cli):
    result = invoke(cli, ["include", "--help"])
    assert result.exit_code == 0
    assert "pyaput include [OPTIONS] REPO PREFIX" in result.stdout


def test_no_args(cli):
    result = invoke(cli, ["include"])
    assert result.exit_code != 0
    assert "Missing argument 'REPO'." in result.stderr
    result = invoke(cli, ["include", "repo"])
    assert result.exit_code != 0
    assert "Missing argument 'PREFIX'." in result.stderr


def test_include(requests_mock, cli):
    repo = "repo"
    prefix = "srsran4g-23.11-1~bpo13+1"
    url = f"https://aptly.home.arpa/api/repos/{repo}/include/{prefix}"
    requests_mock.post(url, json=[])
    result = invoke(cli, ["include", repo, prefix])
    assert result.exit_code == 0
