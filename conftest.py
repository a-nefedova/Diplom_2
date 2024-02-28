import allure
import pytest
import requests

from helper import valid_creds, post_request_register, post_request_auth
from data import URLs


@allure.step('Создаём уникального пользователя и возвращаем его учётные данные')
@pytest.fixture
def registered_user():
    user_creds = {}

    creds = valid_creds()
    response = post_request_register(creds)
    user_creds['creds'] = creds
    user_creds['token'] = response.json()["accessToken"]

    yield user_creds

    response_del = requests.delete(f'{URLs.USER_PATCH_OR_DELETE}', headers=creds['token'], data=creds)
# TODO убрать ассерт и название ответа
    assert response_del.status_code == 202
