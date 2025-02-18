import allure

from methods.order_methods import OrderMethods
from tests.data import OrderData


class TestNewOrderCreation:
    @allure.title("Создание нового заказа авторизованным пользователем")
    @allure.description("Тест проверяет возможность создания заказа авторизованным пользователем в ручке POST /api/orders с использованием валидных ингредиентов.")
    def test_new_order_creation_with_authorization(self, login_user):
        response, response_data, login_data, user_data, access_token = login_user
        token = access_token
        ingredients_response = OrderMethods.get_ingredients()
        ingredients_data = ingredients_response.json()['data']
        ingredient_ids = [ingredients_data[0]['_id'], ingredients_data[1]['_id']]
        order_data = {
            "ingredients": ingredient_ids
        }
        headers = {
            "Authorization": token
        }
        order_response = OrderMethods.create_order(order_data, headers)
        order_response_data = order_response.json()
        assert (order_response.status_code == 200
                and order_response_data['success'] is True
                and 'order' in order_response_data
                and 'number' in order_response_data['order'])

    @allure.title("Создание нового заказа неавторизованным пользователем")
    @allure.description("Тест проверяет, что в ручке POST /api/orders неавторизованный пользователь не может создать заказ.")
    def test_new_order_creation_without_authorization(self):
        ingredients_response = OrderMethods.get_ingredients()
        ingredients_data = ingredients_response.json()['data']
        ingredient_ids = [ingredients_data[0]['_id'], ingredients_data[1]['_id']]
        order_data = {
            "ingredients": ingredient_ids
        }
        headers = {
            "Authorization": ""
        }
        order_response = OrderMethods.create_order(order_data, headers)
        order_response_data = order_response.json()
        assert (order_response.status_code in [401, 403]
                and order_response_data['success'] is False
                and 'message' in order_response_data)

    @allure.title("Создание нового заказа пользователем без ингредиентов")
    @allure.description("Тест проверяет, что при попытке создать заказ без ингредиентов в ручке POST /api/orders, API возвращает корректный код и текст ошибки.")
    def test_new_order_creation_without_ingredients(self, login_user):
        response, response_data, login_data, user_data, access_token = login_user
        token = response_data['accessToken']
        order_data = {
            "ingredients": ""
        }
        headers = {
            "Authorization": token
        }
        order_response = OrderMethods.create_order(order_data, headers)
        order_response_data = order_response.json()
        order_response_message = 'Ingredient ids must be provided'
        assert (order_response.status_code == 400
                and order_response_data['success'] is False
                and order_response_data['message'] == order_response_message)

    @allure.title("Создание нового заказа пользователем с указанием некорректного хэша ингредиента")
    @allure.description("Тест проверяет, что при попытке создать заказ в ручке POST /api/orders с указанием некорректного хэша ингредиента API возвращает корректный код ошибки.")
    def test_new_order_creation_with_incorrect_ingredients_hash(self, login_user):
        response, response_data, login_data, user_data, access_token = login_user
        token = response_data['accessToken']
        order_data = {
            "ingredients": OrderData.INCORRECT_HASH
        }
        headers = {
            "Authorization": token
        }
        order_response = OrderMethods.create_order(order_data, headers)
        response_text = order_response.text
        assert (order_response.status_code == 500 and
                'Internal Server Error' in response_text)
