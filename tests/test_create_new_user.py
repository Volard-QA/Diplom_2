import allure

from data import UserResponse

class TestCreateUser:
    @allure.title("Проверка успешного создания нового пользователя")
    @allure.description("Создаем нового пользователя с валидными данными полей Email, Password, User_name в ручке POST /api/auth/register, проверяем корректность кода и тела ответа")
    def test_create_new_user(self, generate_user):
        response, response_data, user_data = generate_user
        assert (response.status_code == 200
        and response_data["success"] is True
        and response_data["user"]["email"] == user_data["email"]
        and response_data["user"]["name"] == user_data["name"]
        and "accessToken" in response_data
        and "refreshToken" in response_data)

    @allure.title("Проверка невозможности создания курьера с одинаковыми логином, паролем")
    @allure.description(
        "Создаем нового курьера с дублирующими данными полей Email, Password в ручке POST /api/auth/register, проверяем корректность кода и тела ответа об ошибке")
    def test_create_same_user_twice(self, generate_user_data, user_methods):
        response, response_data, user_data = generate_user_data
        duplicate_response = user_methods.create_user(user_data)
        duplicate_response_data = duplicate_response.json()
        duplicate_response_data_text = duplicate_response.json()['message']
        expected_response = UserResponse.TWICE_CREATED_USER_RESPONSE
        assert (duplicate_response.status_code == 403
        and duplicate_response_data["success"] is False
        and duplicate_response_data_text == expected_response)

    @allure.title("Проверка невозможности создания пользователя без одного из обязательных полей")
    @allure.description("Создаем нового пользователя без указания логина в ручке POST /api/auth/register, проверяем корректность кода и тела ответа об ошибке отсутствия данных обязательного поля")
    def test_create_courier_without_required_field(self, user_methods):
        user_data = {
            "email": "",
            "password": "somepassword",  # Укажите пароль
            "name": "Vlad"
        }
        response = user_methods.create_user(user_data)
        response_data = response.json()
        response_data_text = response.json()['message']
        expected_response = UserResponse.CREATE_USER_WITHOUT_EMAIL
        assert (response.status_code == 403
                and response_data["success"] is False
                and response_data_text == expected_response)
