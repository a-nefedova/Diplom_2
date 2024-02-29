import allure
import pytest
import requests

from helper import valid_creds, post_request_register
from data import URLs


@allure.step('Создаём уникального пользователя и возвращаем его учётные данные')
@pytest.fixture
def registered_user():
    user_creds = {}

    creds = valid_creds()
    response = post_request_register(creds)
    user_creds['creds'] = creds
    user_creds['headers'] = {'Authorization': response.json()["accessToken"]}

    yield user_creds

    requests.delete(f'{URLs.USER_PATCH_OR_DELETE}', headers=user_creds['headers'], data=user_creds['creds'])
