import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
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

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
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
            flash(error_message, 'error')  # Flash the error message
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
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route('/book_list')
def book_list():
    return "Book List Page"


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book_id = request.form.get('book_id')  # Get selected book ID from the form

        if not book_id:
            flash("No book selected!", category="error")
            return redirect(url_for('add_book'))

        # Check if the book is already in the user's list
        existing_entry = db.session.execute(
            text("SELECT * FROM user_books WHERE user_id = :user_id AND book_id = :book_id"),
            {"user_id": current_user.user_id, "book_id": book_id}
        ).fetchone()

        if existing_entry:
            flash("This book is already in your list!", category="error")
        else:
            # Add the book to user_books
            db.session.execute(
                text("""
                    INSERT INTO user_books (user_id, book_id, reading_progress, completed, wishlist)
                    VALUES (:user_id, :book_id, 0, FALSE, FALSE)
                """),
                {"user_id": current_user.user_id, "book_id": book_id}
            )
            db.session.commit()
            flash("Book successfully added to your list!", category="success")

        return redirect(url_for('reading_status'))

    return render_template('add_book.html')


@app.route('/search_books', methods=['GET'])
@login_required
def search_books():
    query = request.args.get('query', '').strip()

    if not query:
        return {"books": []}  # Empty response if query is empty

    # Query matching books from the database
    books = db.session.execute(
        text("SELECT book_id, book_name, writer_name FROM book_list WHERE book_name LIKE :query LIMIT 5"),
        {"query": f"%{query}%"}
    ).fetchall()

    # Convert the result into JSON format
    books_list = [{"id": book.book_id, "name": book.book_name, "writer": book.writer_name} for book in books]
    return {"books": books_list}



@app.route('/reading_status')
@login_required
def reading_status():
    
    return render_template('reading_status.html')

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


