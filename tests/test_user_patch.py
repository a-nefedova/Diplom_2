import allure
import pytest

from helper import valid_creds, random_string, post_request_register
from data import URLs


class TestUserPatch:

    @allure.title('Проверяем, что с авторизацией можно изменить любое поле из учётных данных пользователя')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль, либо имя изменено. '
                        'Проверяем, что в ответ приходит код 200 и тело ответа содержит изменённые данные')
    @allure.link(URLs.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_user_patch_authorized(self, cred, registered_user):

        registered_user[cred] = random_string()

        response = post_request_register(user)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 403 and message == "Email, password and name are required fields"
