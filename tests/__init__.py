from typer.testing import CliRunner, Result
from pyaput.cli import app


def invoke(cli: CliRunner, args: list) -> Result:
    return cli.invoke(app, args, catch_exceptions=False, prog_name="pyaput")
