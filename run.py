# from flask import Flask, render_template, request, redirect, url_for, flash
# import mysql.connector
# from mysql.connector import Error
# from werkzeug.security import generate_password_hash

# app = Flask(__name__)

# # Set a secret key for session and flash messaging
# app.secret_key = 'your_secret_key'  # Replace with a secure key

# # Database connection function
# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',  # your MySQL username
#             password='',  # your MySQL password
#             database='bookvault_db'  # replace with your database name
#         )
#         if conn.is_connected():
#             print("Connected to the database")
#         return conn
#     except Error as e:
#         print(f"Error: {e}")
#         return None

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book_vault'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "error"  

# User model for Flask-Login
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Override the get_id method to return user_id instead of the default 'id'
    def get_id(self):
        return str(self.user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            
            # # Connect to the database and insert the new user data
            # conn = get_db_connection()
            # if conn:
            #     cursor = conn.cursor()
            #     query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            #     values = (username, email, hashed_password)
            #     cursor.execute(query, values)
            #     conn.commit()
            #     print(f"User {username} added to the database")
            #     cursor.close()
            #     conn.close()

            #     # Flash success message and redirect to login page
            #     flash('You have successfully signed up! Please log in.', 'success')
            #     return redirect(url_for('login'))
            # else:
            #     error_message = "Could not connect to the database."
            #     flash(error_message, 'danger')  # Flash the error message
            #     return render_template('signup.html')

            existing_user_email = User.query.filter_by(email=email).first()
            existing_user_username = User.query.filter_by(username=username).first()
            
            if existing_user_email:
                flash("This email already exists. Please log in or use another email.", category="error")
            elif existing_user_username:
                flash("This username already exists. Please choose another one.", category="error")
            else:

                hashed_password = generate_password_hash(password)

                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                flash("Account created successfully! Please log in.", category="success")
                return redirect(url_for("login"))  
        else:
            error_message = "Passwords do not match!"
            flash(error_message, 'danger')  # Flash the error message
            return render_template('signup.html')

    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]  
        password = request.form["password"]  
        user = User.query.filter_by(username=username).first() 

        if user and check_password_hash(user.password, password):  
            login_user(user)
            flash("Login successful!", category="success")
            return redirect(url_for("home"))
        else:
            flash("Wrong Username or Password. Please Try Again!", category="error")
    
    return render_template("login.html")

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for("home"))

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)


