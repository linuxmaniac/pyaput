import pytest


# See https://github.com/pallets/click/issues/824
@pytest.fixture(autouse=True)
def fix_error(caplog):
    caplog.set_level(100000, logger="requests_mock")
