import allure
import pytest

from helper import valid_creds, post_request_register
from data import URLs


class TestUserRegister:

    @allure.title('Проверяем, что чтобы создать пользователя, нужно передать в ручку все обязательные поля')
    @allure.description('Регистрируем пользователя с заполненными email, паролем и именем, '
                        'проверяем, что в ответ приходит код 200 и тело ответа содержит accessToken')
    @allure.link(URLs.USER_REGISTER)
    def test_all_required_creds(self):

        user = valid_creds()
        register = post_request_register(user)

        assert register.status_code == 200 and 'accessToken' in register.text

    @allure.title('Проверяем, что нельзя создать пользователя, который уже зарегистрирован')
    @allure.description('Пытаемся зарегистрировать пользователя под уже существующим учётными данными, '
                        'проверяем, что возвращается ошибка 403: User already exists')
    @allure.link(URLs.USER_REGISTER)
    def test_register_two_same_users(self, registered_user):

        user = registered_user.copy()['creds']

        register = post_request_register(user)
        status_code = register.status_code
        message = register.json()['message']

        assert status_code == 403 and message == "User already exists"

    @allure.title('Проверяем, что если одно из обязательных полей не заполнено, запрос возвращает ошибку')
    @allure.description('Используем параметризацию, где в тестовых данных email, пароль или имя отсутствует. '
                        'Проверяем, что возвращается ошибка 403: Email, password and name are required fields')
    @allure.link(URLs.USER_REGISTER)
    @pytest.mark.parametrize('cred', ['email', 'password', 'name'])
    def test_unfilled_required_creds(self, cred):

        user = valid_creds()
        user[cred] = None

        register = post_request_register(user)
        status_code = register.status_code
        message = register.json()['message']

        assert status_code == 403 and message == "Email, password and name are required fields"
