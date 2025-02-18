import requests
from curl import Url


class UserMethods:
    @staticmethod
    def create_user(user_data):
        return requests.post(f'{Url.BASE_URL}{Url.USER_REGISTRATION_URL}', json=user_data)

    @staticmethod
    def delete_user(headers):
        return requests.delete(f"{Url.BASE_URL}{Url.USER_INFORMATION_URL}", headers=headers)

    @staticmethod
    def login_user(login_data):
        return requests.post(f'{Url.BASE_URL}{Url.USER_LOGIN_URL}', json=login_data)

    @staticmethod
    def get_user_data(headers):
        return requests.get(f'{Url.BASE_URL}{Url.USER_INFORMATION_URL}', headers=headers)

    @staticmethod
    def update_user_data(headers,update_user_data):
        return requests.patch(f'{Url.BASE_URL}{Url.USER_INFORMATION_URL}', headers=headers, json=update_user_data)


