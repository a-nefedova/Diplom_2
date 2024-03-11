import pytest

from helper import valid_creds, post_request_register, delete_request_user


@pytest.fixture
def registered_user():

    creds = valid_creds()
    register = post_request_register(creds)
    user = {
        'creds': creds,
        'headers': {'Authorization': register.json()["accessToken"]}
    }

    yield user

    delete_request_user(user['headers'])
