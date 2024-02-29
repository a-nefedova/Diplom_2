import requests

from data import URLs, ingredients


class TestOrder:

    def test_create_order_authorized(self, registered_user):

        user_headers = registered_user['headers']
        response = requests.post(URLs.ORDERS, headers=user_headers, data=ingredients)

        assert response.status_code == 200 # todo тут ещё в ответе придут данные об ингредиентах, в ассерт надо

    def test_create_order_unauthorized(self):

        response = requests.post(URLs.ORDERS, data=ingredients)

        assert response.status_code == 200  # todo а тут заказ без подробностей

    def test_create_order_no_ingredients(self):

        response = requests.post(URLs.ORDERS, data={})

        assert response.status_code == 400 and "Ingredient ids must be provided" in response.json()['message']
