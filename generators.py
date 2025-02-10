from faker import Faker
fake = Faker()

def generate_new_user_data():
    return {
    "email": fake.unique.email(),
    "password": fake.password(length=8),
    "name": fake.last_name()
    }

