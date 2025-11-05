from typer.testing import CliRunner, Result
from pyaput.cli import app

runner = CliRunner()


def invoke(args: list) -> Result:
    return runner.invoke(app, args, catch_exceptions=False, prog_name="pyaput")
