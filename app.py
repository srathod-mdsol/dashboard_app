from flask import Flask, render_template, request
import sqlite3
import threading

app = Flask(__name__)

# Create a database connection for each thread
def get_db_connection():
    conn = sqlite3.connect('instance\sample.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create a new database cursor for each thread
def get_db_cursor(connection):
    return connection.cursor()

# Initialize the database
def init_db():
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    
    # Create a table in the database if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    connection.commit()
    cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')

    connection = get_db_connection()
    cursor = get_db_cursor(connection)

    # Insert the user into the database
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    connection.commit()
    cursor.close()
    connection.close()

    return 'User added successfully!'

@app.route('/users')
def users():
    connection = get_db_connection()
    cursor = get_db_cursor(connection)

    # Retrieve all users from the database
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
