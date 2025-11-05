import asyncio
import requests
from urllib.parse import urljoin
from pathlib import Path
from functools import wraps

import typer
from typing_extensions import Annotated
from rich import print
from rich.console import Console
from debian.deb822 import Changes
from .settings import settings

err_console = Console(stderr=True)
console = Console()
app = typer.Typer()


def syncify(f):
    """This simple decorator converts an async function into a sync function,
    allowing it to work with Typer.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@app.command(help=f"Display the current installed version of {settings.project_name}.")
def version():
    from . import __version__

    print(f"{settings.project_name} - {__version__}")


def get_prefix(changes: Changes) -> str:
    try:
        source = changes["Source"]
        version = changes["Version"]
    except KeyError as err:
        err_console.print(f"{err} not found")
        raise typer.Exit(1)
    return f"{source}-{version}"


def get_changes(changes_file) -> Changes:
    with changes_file.open() as fh:
        changes = Changes(fh)
    return changes


def send_file(prefix: str, file: Path):
    url = urljoin(settings.aptly_api_url, f"files/{prefix}/")
    with file.open("rb") as f:
        r = requests.post(url, files={"file": f})
    console.print(f"{file.name} sent to {url}:{r.status_code}")
    assert r.status_code == requests.codes.ok


def process_changes(changes: Changes, changes_file: Path) -> set:
    ok_files = set()
    missing_files = set()
    console.print(f"processing {changes_file}")
    base_dir = changes_file.parent
    if "Files" not in changes:
        err_console.print(f"'Files' not found at {changes_file}")
        raise typer.Exit(1)
    for info in changes["Files"]:
        file_path = base_dir / info["name"]
        if file_path.is_file():
            console.print(f"+ {file_path}")
            ok_files.add(file_path)
        else:
            err_console.print(f"file {file_path} not found")
            missing_files.add(file_path)
    if len(missing_files) > 0:
        err_console.print(f"missing files: {missing_files}")
        raise typer.Exit(2)
    ok_files.add(changes_file)
    return ok_files


@app.command(help="send files.")
def files(
    changes: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
):
    changes_info = get_changes(changes)
    changes_files = process_changes(changes_info, changes)
    if len(changes_files) == 0:
        raise typer.Exit(1)
    prefix = get_prefix(changes_info)
    for file in changes_files:
        send_file(prefix, file)


@app.command(help=f"show config of {settings.project_name}.")
def config():
    print(f"{settings}")
