from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Set a secret key for session and flash messaging
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # your MySQL username
            password='',  # your MySQL password
            database='bookvault_db'  # replace with your database name
        )
        if conn.is_connected():
            print("Connected to the database")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    print("Home route is working!")
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            # Hashing password using pbkdf2:sha256
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Connect to the database and insert the new user data
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                values = (username, email, hashed_password)
                cursor.execute(query, values)
                conn.commit()
                print(f"User {username} added to the database")
                cursor.close()
                conn.close()

                # Flash success message and redirect to login page
                flash('You have successfully signed up! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                error_message = "Could not connect to the database."
                flash(error_message, 'danger')  # Flash the error message
                return render_template('signup.html')
        else:
            error_message = "Passwords do not match!"
            flash(error_message, 'danger')  # Flash the error message
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')  # Create a login.html template for the login form

@app.route('/book_list')
def book_list():
    return "Book List Page"

@app.route('/reading_status')
def reading_status():
    return "Reading Status Page"

@app.route('/completed_books')
def completed_books():
    return "Completed Books Page"

@app.route('/wishlist')
def wishlist():
    return "Wishlist Page"

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)


