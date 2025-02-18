import pytest

from generators import generate_new_user_data
from methods.user_methods import UserMethods


@pytest.fixture(scope='function')
def user_methods():
    return UserMethods()

@pytest.fixture(scope='function')
def generate_user(user_methods):
    login_pass = generate_new_user_data()
    user_data = {
        "email": login_pass['email'],
        "password": login_pass['password'],
        "name": login_pass['name']
    }
    response = user_methods.create_user(user_data)
    response_data = response.json()
    yield response, response_data, user_data
    access_token = response_data['accessToken']
    headers = {'Authorization': access_token}
    user_methods.delete_user(headers)

@pytest.fixture(scope='function')
def generate_user_data(user_methods):
    login_pass = generate_new_user_data()
    user_data = {
        "email": login_pass['email'],
        "password": login_pass['password'],
        "name": login_pass['name']
    }
    response = user_methods.create_user(user_data)
    response_data = response.json()
    return response, response_data, user_data

@pytest.fixture(scope='function')
def login_user(user_methods):
    login_pass = generate_new_user_data()
    user_data = {
        "email": login_pass['email'],
        "password": login_pass['password'],
        "name": login_pass['name']
    }
    user_methods.create_user(user_data)
    login_data = {
        "email": user_data['email'],
        "password": user_data['password']
    }
    response = user_methods.login_user(login_data)
    response_data = response.json()
    access_token = response_data['accessToken']
    yield response, response_data, login_data, user_data, access_token
    headers = {'Authorization': access_token}
    user_methods.delete_user(headers)