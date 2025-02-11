import allure

from methods.user_methods import UserMethods

class TestUserLogin:
    @allure.title("Проверка успешной авторизации пользователя с корректными логином и паролем")
    @allure.description(
        "Создаем нового пользователя и производим его авторизацию в ручке POST /api/auth/login, проверяем корректность кода и тела ответа об успешной авторизации")
    def test_successful_login(self, login_user):
        response, response_data, login_data, user_data, access_token = login_user
        assert (response.status_code == 200
        and response_data["success"] is True
        and response_data["user"]["email"] == login_data["email"]
        and response_data["user"]["name"] == user_data["name"]
        and "accessToken" in response_data
        and "refreshToken" in response_data)

    @allure.title("Проверка невозможности авторизации пользователя с E-mail, несуществующим в БД")
    @allure.description(
        "Создаем нового пользователя и производим его авторизацию в ручке POST /api/auth/login с указанием E-mail, отсутствующего в БД, проверяем корректность кода и тела ответа об ошибке авторизации с несуществующей парой логин-пароль")
    def test_login_with_nonexistent_login(self, user_methods, generate_user_data):
        response, response_data, user_data = generate_user_data
        login_data = {
            "email": "nonexistent_email",
            "password": user_data['password']
        }
        response = UserMethods.login_user(login_data)
        response_data = response.json()
        response_data_text = response.json()['message']
        expected_response = 'email or password are incorrect'
        assert (response.status_code == 401
                and response_data["success"] is False
                and response_data_text == expected_response)
