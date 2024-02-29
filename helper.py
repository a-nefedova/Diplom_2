from data import URLs

import requests
import random
import string
import allure


def random_string(length=10):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters)[:length] for i in range(length))
    return random_str


@allure.step('Генерируем словарь с уникальными учётными данными')
def valid_creds():
    creds = {
        'email': f'{random_string()}@yandex.ru',
        'password': random_string(),
        'name': random_string()
    }
    return creds


@allure.step(f'Отправляем данные на регистрацию пользователя')
def post_request_register(creds):
    response = requests.post(URLs.USER_REGISTER, data=creds)
    return response


@allure.step(f'Отправляем данные на авторизацию')
def post_request_auth(creds):
    response = requests.post(URLs.USER_AUTH, data=creds)
    return response


@allure.step(f'Отправляем данные на заказ')
def post_request_order(creds):
    return requests.post(URLs.ORDER, data=creds)


@allure.step('Отправляем запрос на получение списка заказов')
def get_request_orders():
    return requests.get(URLs.ORDER)
