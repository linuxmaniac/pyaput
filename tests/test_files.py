from pathlib import Path
from . import invoke

FIXTURES = Path(__file__).resolve(strict=True).parent / "fixtures"


def test_files_help():
    result = invoke(["files", "--help"])
    assert result.exit_code == 0
    assert "--changes" in result.stdout


def test_no_args():
    result = invoke(["files"])
    assert result.exit_code != 0
    assert "Missing option '--changes'." in result.stderr


def test_file_not_exists():
    result = invoke(["files", "--changes", "/file-not-found"])
    assert result.exit_code != 0
    assert "File '/file-not-found' does not exist." in result.stderr


def test_not_changes():
    changes_file = FIXTURES / "not-changes.txt"
    result = invoke(["files", "--changes", f"{changes_file}"])
    assert "'Files' not found at" in result.stderr
    assert result.exit_code != 0


def test_changes(requests_mock):
    url = "https://aptly.home.arpa/api/files/srsran4g-23.11-1~bpo13+1/"
    requests_mock.post(url, json=[])
    changes_file = FIXTURES / "srsran4g_23.11-1~bpo13+1_amd64.changes"
    result = invoke(["files", "--changes", f"{changes_file}"])
    assert result.exit_code == 0
