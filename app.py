from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Function to create a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="a@111111",
            database="login_db"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()

            # Validate user in MySQL
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                # Redirect to indore page after successful login
                return redirect('/indore')
            else:
                flash("Invalid username or password")
                return redirect('/login')  # Redirect back to login with message

    # Render the login form (GET request)
    return render_template('login.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()

            # Insert new user into MySQL
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()

            cursor.close()
            connection.close()

            flash("Registration successful. Please log in.")
            return redirect('/login')  # Redirect to the login page after registration

    # Render the registration form (GET request)
    return render_template('register.html')

# Indore page (after successful login)
@app.route('/indore')
def indore():
    return render_template('indore.html')

if __name__ == '__main__':
    app.run(debug=True)

