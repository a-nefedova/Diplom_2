import allure
import pytest
import requests

from helper import random_string
from data import URLs


class TestUserPatch:

    @allure.title('Проверяем, что с авторизацией можно изменить любое поле из учётных данных пользователя')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль, либо имя изменено. '
                        'Проверяем, что в ответ приходит код 200 и тело ответа содержит {"success": true}')
    @allure.link(URLs.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_user_patch_authorized(self, cred, registered_user):

        registered_user['creds'][cred] = random_string()
        user_headers = registered_user['headers']
        user_creds = registered_user['creds']

        response = requests.patch(URLs.USER_PATCH_OR_DELETE, headers=user_headers, data=user_creds)
        assert response.status_code == 200 and '"success":true' in response.text

    @allure.title('Проверяем, что никакое поле из учётных данных пользователя нельзя изменить без авторизации')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль, либо имя изменено. '
                        'Проверяем, что в ответ приходит код 401: You should be authorised')
    @allure.link(URLs.USER_PATCH_OR_DELETE)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_user_patch_unauthorized(self, cred, registered_user):

        registered_user['creds'][cred] = random_string()
        user_creds = registered_user['creds']

        response = requests.patch(URLs.USER_PATCH_OR_DELETE, data=user_creds)
        assert response.status_code == 401 and 'You should be authorised' in response.text
