import os
import pytest


@pytest.fixture(scope='session', autouse=False)
def cred():
    """Pytest fixture method to return Nexmo Api
    credentials stored in OS Environment Variables.
    Gets them only once, saves and yields as a tuple,
    delete afterwards. Works once for each test session.
    """
    credentials = (os.getenv('NEXMO_API_KEY', 0),
                   os.getenv('NEXMO_API_SECRET', 0))
    yield credentials
    del credentials
