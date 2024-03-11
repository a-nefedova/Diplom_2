import pytest
import allure

from data import URLs
from helper import valid_creds, post_request_auth


class TestUserAuthorization:

    @allure.title('Проверяем, что можно авторизоваться под существующим пользователем')
    @allure.description('Авторизуемся с существующими email и паролем, '
                        'проверяем, что в ответ приходит код 200 и тело ответа содержит accessToken')
    @allure.link(URLs.USER_AUTH)
    def test_auth_registered_creds(self, registered_user):

        auth = post_request_auth(registered_user['creds'])

        assert auth.status_code == 200 and 'accessToken' in auth.text

    @allure.title('Проверяем, что система вернёт ошибку, если неправильно указать email или пароль')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль некорректный. '
                        'Проверяем, что возвращается ошибка 401: email or password are incorrect')
    @allure.link(URLs.USER_AUTH)
    @pytest.mark.parametrize('cred', ['email', 'password'])
    def test_auth_incorrect_creds(self, registered_user, cred):

        user = registered_user['creds']
        user[cred] = valid_creds()[cred]

        auth = post_request_auth(user)
        status_code = auth.status_code
        message = auth.json()["message"]

        assert status_code == 401 and message == "email or password are incorrect"
