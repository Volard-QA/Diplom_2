import allure

from methods.user_methods import UserMethods


class TestUserInformationChange:
    @allure.title("Проверка изменения данных авторизованного пользователя")
    @allure.description(
        "Тест проверяет возможность изменения данных пользователя через PATCH запрос ручки api/auth/user и получение обновленных данных через GET запрос.")
    def test_update_user_data(self, login_user):
        response, response_data, login_data, user_data, access_token = login_user
        token = response_data['accessToken']
        headers = {
        "Authorization": token
        }
        update_user_data = {
            "email": "mynew_email@yandex.ru",
            "name": "New Name"
        }
        UserMethods.update_user_data(headers, update_user_data)
        get_updated_response = UserMethods.get_user_data(headers)
        updated_user = get_updated_response.json()
        updated_user_info = get_updated_response.json()['user']
        assert (get_updated_response.status_code == 200
        and updated_user["success"] is True
        and updated_user_info["name"] == update_user_data["name"]
        and updated_user_info["email"] == update_user_data["email"])

    @allure.title("Проверка изменения данных пользователя без авторизации")
    @allure.description(
        "Тест проверяет, что система возвращает ошибку при попытке изменения данных пользователя в ручке PATCH api/auth/user без авторизации.")
    def test_update_unauthorized_user_data(self, generate_user):
        headers = {
            "Authorization": ""
        }
        update_user_data = {
            "email": "windy_email@yandex.ru",
            "name": "New Name"
        }
        response = UserMethods.update_user_data(headers, update_user_data)
        patch_response = response.json()
        patch_response_info = response.json()['message']
        patch_response_text = 'You should be authorised'
        assert (response.status_code == 401
                and patch_response["success"] is False
                and patch_response_info == patch_response_text)
