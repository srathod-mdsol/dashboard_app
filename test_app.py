import pytest
import allure
from app import app, init_db, get_db_connection

@pytest.fixture(scope="module")
def test_app():
    app.config['TESTING'] = True
    with app.app_context():
        init_db()  # Initialize the test database
    yield app

@pytest.fixture(scope="module")
def test_client(test_app):
    return test_app.test_client()

@allure.feature("Index")
def test_index(test_client):
    with allure.step("Accessing the index page"):
        response = test_client.get('/')
    assert response.status_code == 200
    assert b'<h1>Add User</h1>' in response.data

@allure.feature("Add User")
def test_add_user(test_client):
    with allure.step("Adding a user"):
        response = test_client.post('/add_user', data={'name': 'John Doe', 'email': 'john@example.com'})
    assert response.status_code == 200
    assert b'User added successfully!' in response.data

    with allure.step("Verifying user details in the database"):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        cursor.close()
        connection.close()

    assert len(users) == 18
    assert users[0]['name'] == 'John Doe'
    assert users[0]['email'] == 'john@example.com'

@allure.feature("Users")
def test_users(test_client):
    with allure.step("Accessing the users page"):
        response = test_client.get('/users')
    assert response.status_code == 200
    assert b'<h1>Users</h1>' in response.data
    assert b'<table>' in response.data

@allure.feature("Invalid Route")
def test_invalid_route(test_client):
    with allure.step("Accessing an invalid route"):
        response = test_client.get('/invalid')
    assert response.status_code == 404

