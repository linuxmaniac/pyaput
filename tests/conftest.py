import pytest
import functools
import sys
from typer.testing import CliRunner


# See https://github.com/pallets/click/issues/824
@pytest.fixture(autouse=True)
def fix_error(caplog):
    caplog.set_level(100000, logger="requests_mock")


@pytest.fixture
def cli():
    """Yield a click.testing.CliRunner to invoke the CLI."""
    class_ = CliRunner

    def invoke_wrapper(f):
        """Augment CliRunner.invoke to emit its output to stdout.

        This enables pytest to show the output in its logs on test
        failures.

        """

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            echo = kwargs.pop("echo", False)
            result = f(*args, **kwargs)

            if echo is True:
                sys.stdout.write(result.output)

            return result

        return wrapper

    class_.invoke = invoke_wrapper(class_.invoke)
    cli_runner = class_()

    yield cli_runner
