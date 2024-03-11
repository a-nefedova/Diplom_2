from data import URLs

import requests
import random
import string
import allure


def random_string(length=10):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters)[:length] for i in range(length))
    return random_str


def valid_creds():
    creds = {
        'email': f'{random_string()}@yandex.ru',
        'password': random_string(),
        'name': random_string()
    }
    return creds


@allure.step(f'Регистрируем нового пользователя')
def post_request_register(creds):
    return requests.post(URLs.USER_REGISTER, data=creds)


@allure.step(f'Авторизуемся')
def post_request_auth(creds):
    return requests.post(URLs.USER_AUTH, data=creds)


@allure.step(f'Изменяем данные пользователя')
def patch_request_user(creds, headers=None):
    return requests.patch(URLs.USER_PATCH_OR_DELETE, headers=headers, data=creds)


@allure.step(f'Удаляем пользователя')
def delete_request_user(headers):
    return requests.delete(URLs.USER_PATCH_OR_DELETE, headers=headers)


@allure.step(f'Создаём заказ')
def post_request_order(headers=None, ingredients=None):
    return requests.post(URLs.ORDERS, headers=headers, data=ingredients)


@allure.step(f'Запрашиваем список заказов')
def get_request_orders(headers=None):
    return requests.get(URLs.ORDERS, headers=headers)
