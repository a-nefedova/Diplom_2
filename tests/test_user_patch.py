import allure
import pytest

from helper import random_string, patch_request_user
from data import URLs


class TestUserPatch:

    @allure.title('Проверяем, что с авторизацией можно изменить учётные данные пользователя')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль, либо имя изменено. '
                        'Проверяем, что в ответ приходит код 200 и тело ответа содержит учётные данные')
    @allure.link(URLs.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_user_patch_authorized(self, cred, registered_user):

        if cred == 'email':
            registered_user['creds'][cred] = f'{random_string()}@yandex.ru'
        else:
            registered_user['creds'][cred] = random_string()
        user_headers = registered_user['headers']
        user_creds = registered_user['creds']
        email_and_name = user_creds.copy()
        email_and_name.pop('password')

        patch = patch_request_user(user_creds, user_headers)

        assert patch.status_code == 200 and patch.json()['user'] == email_and_name

    @allure.title('Проверяем, что без авторизации нельзя изменить учётные данные пользователя')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль, либо имя изменено. '
                        'Проверяем, что в ответ приходит код 401: You should be authorised')
    @allure.link(URLs.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_user_patch_unauthorized(self, cred, registered_user):

        if cred == 'email':
            registered_user['creds'][cred] = f'{random_string()}@yandex.ru'
        else:
            registered_user['creds'][cred] = random_string()
        user_creds = registered_user['creds']

        patch = patch_request_user(user_creds)

        assert patch.status_code == 401 and 'You should be authorised' in patch.text
