import requests
from curl import Url

class OrderMethods:
    @staticmethod
    def get_ingredients():
        return requests.get(f'{Url.BASE_URL}{Url.INGREDIENT_URL}')

    @staticmethod
    def create_order(order_data, headers):
        return requests.post(f'{Url.BASE_URL}{Url.ORDER_CREATION_URL}', json=order_data, headers=headers)

    @staticmethod
    def get_orders(headers):
        return requests.get(f'{Url.BASE_URL}{Url.ORDER_CREATION_URL}', headers=headers)
