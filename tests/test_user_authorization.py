import pytest
import allure

from data import URLs
from helper import valid_creds, random_string, post_request_auth


class TestUserAuthorization:

    @allure.title('Проверяем, что для авторизации нужно передать все обязательные поля')
    @allure.description('Авторизуемся с существующими email и паролем, '
                        'проверяем, что в ответ приходит код 200 и тело ответа содержит {"success": true}')
    @allure.link(URLs.USER_AUTH)
    def test_auth_all_required_creds(self, registered_user):

        response = post_request_auth(registered_user)

        assert response.status_code == 200 and '"success":true' in response.text

    @allure.title('Проверяем, что система вернёт ошибку, если неправильно указать email или пароль')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль некорректный. '
                        'Проверяем, что возвращается ошибка 401: email or password are incorrect')
    @allure.link(URLs.USER_AUTH)
    @pytest.mark.parametrize('cred', ['email', 'password'])
    def test_auth_incorrect_creds(self, registered_user, cred):

        user = registered_user.copy()
        user[cred] = random_string()

        response = post_request_auth(user)
        status_code = response.status_code
        message = response.json()["message"]

        assert status_code == 401 and message == "email or password are incorrect"
