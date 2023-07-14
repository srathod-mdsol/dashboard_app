import unittest
from app import app, init_db, get_db_connection

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            init_db()  # Initialize the test database

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Add User</h1>', response.data)

    def test_add_user(self):
        response = self.app.post('/add_user', data={'name': 'John Doe', 'email': 'john@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added successfully!', response.data)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        cursor.close()
        connection.close()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], 'John Doe')
        self.assertEqual(users[0]['email'], 'john@example.com')

    def test_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Users</h1>', response.data)
        self.assertIn(b'<table>', response.data)

    def test_invalid_route(self):
        response = self.app.get('/invalid')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
