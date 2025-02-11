import allure

from methods.order_methods import OrderMethods


class TestGettingOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Тест проверяет возможность получения заказов конкретного авторизованного пользователя.")
    def test_get_orders_authorized_user(self, login_user):
        response, response_data, login_data, user_data, access_token = login_user
        token = response_data['accessToken']
        ingredients_response = OrderMethods.get_ingredients()
        ingredients_data = ingredients_response.json()['data']
        ingredient_ids = [ingredients_data[0]['_id'], ingredients_data[1]['_id']]
        order_data = {
            "ingredients": ingredient_ids
        }
        headers = {
            "Authorization": token
        }
        OrderMethods.create_order(order_data, headers)
        orders_response = OrderMethods.get_orders(headers)
        orders_response_data = orders_response.json()
        order = orders_response_data['orders'][0]
        assert (orders_response.status_code == 200
                and orders_response_data['success'] is True
                and 'orders' in orders_response_data
                and 'total' in orders_response_data
                and 'totalToday' in orders_response_data
                and isinstance(orders_response_data['orders'], list)
                and len(orders_response_data['orders']) <= 50
                and 'ingredients' in order
                and '_id' in order
                and 'status' in order
                and 'number' in order
                and 'createdAt' in order
                and 'updatedAt' in order
                and order['status'] in ["done", "pending", "canceled"])

    @allure.title("Получение заказов неавторизованного пользователя")
    @allure.description("Тест проверяет, что неавторизованный пользователь не может получить список заказов.")
    def test_get_orders_unauthorized_user(self):
        headers = {
            "Authorization": ""
        }
        orders_response = OrderMethods.get_orders(headers)
        orders_response_data = orders_response.json()
        assert (orders_response.status_code == 401
                and orders_response_data['success'] is False
                and orders_response_data['message'] == 'You should be authorised')
