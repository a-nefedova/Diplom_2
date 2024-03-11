import allure

from data import ingredients, URLs
from helper import post_request_order, get_request_orders


class TestOrder:

    @allure.title('Проверяем, что с авторизацией и ингредиентами можно создать заказ')
    @allure.description('Проверяем, что в ответ приходит код 200 и тело ответа содержит номер и владельца заказа')
    @allure.link(URLs.ORDERS)
    def test_create_order_authorized(self, registered_user):

        headers = registered_user['headers']

        order = post_request_order(headers, ingredients)
        status_code = order.status_code
        order_info = order.json()['order']

        assert (status_code == 200
                and 'number' in order_info
                and 'owner' in order_info)

    @allure.title('Проверяем, что без авторизации и с ингредиентами можно создать заказ')
    @allure.description('Проверяем, что в ответ приходит код 200 '
                        'и тело ответа содержит номер заказа, но не содержит владельца заказа')
    @allure.link(URLs.ORDERS)
    def test_create_order_unauthorized(self):

        order = post_request_order(ingredients=ingredients)
        status_code = order.status_code
        order_info = order.json()['order']

        assert (status_code == 200
                and 'number' in order_info
                and 'owner' not in order_info)

    @allure.title('Проверяем, что нельзя создать заказ c авторизацией и без ингредиентов')
    @allure.description('Проверяем, что в ответ приходит код 400: Ingredient ids must be provided')
    @allure.link(URLs.ORDERS)
    def test_create_order_no_ingredients(self, registered_user):

        headers = registered_user['headers']

        order = post_request_order(headers)
        status_code = order.status_code
        message = order.json()['message']

        assert status_code == 400 and "Ingredient ids must be provided" in message

    @allure.title('Проверяем, что нельзя создать заказ с авторизацией и неверным хэшем ингредиента')
    @allure.description('Проверяем, что в ответ приходит код 400: One or more ids provided are incorrect')
    @allure.link(URLs.ORDERS)
    def test_create_order_incorrect_hash_ingredients(self, registered_user):

        headers = registered_user['headers']

        order = post_request_order(headers, {'ingredients': ["deadfacedfadedcafefacade"]})
        status_code = order.status_code
        message = order.json()['message']

        assert status_code == 400 and "One or more ids provided are incorrect" in message

    @allure.title('Проверяем, что с авторизацией можно получить список заказов конкретного пользователя')
    @allure.description('Проверяем, что в ответ приходит код 200 и созданный заказ есть в списке')
    @allure.link(URLs.ORDERS)
    def test_get_user_orders_authorized(self, registered_user):

        user_headers = registered_user['headers']

        create_order = post_request_order(user_headers, ingredients)
        order_number = create_order.json()['order']['number']

        get_orders = get_request_orders(user_headers)
        status_code = get_orders.status_code
        user_orders = get_orders.json()['orders']

        assert (status_code == 200
                and type(user_orders) is list
                and user_orders[-1]['number'] == order_number)

    @allure.title('Проверяем, что без авторизации нельзя получить список заказов конкретного пользователя')
    @allure.description('Проверяем, что в ответ приходит код 401:  You should be authorised')
    @allure.link(URLs.ORDERS)
    def test_get_user_orders_unauthorized(self):

        get_orders = get_request_orders()
        status_code = get_orders.status_code
        message = get_orders.json()['message']

        assert status_code == 401 and message == "You should be authorised"
