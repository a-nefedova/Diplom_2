import allure
import pytest

from helper import valid_creds, random_string, post_request_register
from data import URLs


class TestUserRegister:

    @allure.title('Проверяем, что чтобы создать пользователя, нужно передать в ручку все обязательные поля')
    @allure.description('Регистрируем пользователя с заполненными email, паролем и именем, '
                        'проверяем, что в ответ приходит код 200 и тело ответа содержит accessToken')
    @allure.link(URLs.USER_REGISTER)
    def test_all_required_creds(self):
        user = valid_creds()
        response = post_request_register(user)

        assert response.status_code == 200 and 'accessToken' in response.text

    @allure.title('Проверяем, что нельзя создать двух пользователей с одинаковыми email')
    @allure.description('Пытаемся зарегистрировать пользователя под уже существующим email, '
                        'проверяем, что возвращается ошибка 403: User already exists')
    @allure.link(URLs.USER_REGISTER)
    def test_register_two_same_users_not_allowed(self, registered_user):

        user = registered_user.copy()['creds']
        user['password'] = random_string()

        response = post_request_register(user)
        response_status_code = response.status_code
        response_message = response.json()['message']

        assert response_status_code == 403 and response_message == "User already exists"

    @allure.title('Проверяем, что если одно из обязательных полей не заполнено, запрос возвращает ошибку')
    @allure.description('Используем параметризацию, где в тестовых данных либо email, либо пароль отсутствует. '
                        'Проверяем, что возвращается ошибка 403: Email, password and name are required fields')
    @allure.link(URLs.USER_REGISTER)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_unfilled_required_creds(self, cred):

        user = valid_creds()
        user[cred] = ''

        response = post_request_register(user)
        status_code = response.status_code
        message = response.json()['message']

        assert status_code == 403 and message == "Email, password and name are required fields"
