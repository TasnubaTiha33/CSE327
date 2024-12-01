import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_login import login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from flask import jsonify
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

"""
User Model
------------------------------------------------
User model for Flask-Login

"""
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

"""
Homepage
------------------------------------------------
Homepage from where we can visit other pages

"""
@app.route('/')
def home():
    print("Home route is working!")
    return render_template('home.html')


"""
Signup 
------------------------------------------------
User will create his/her account using the form of signup

"""
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

"""
Login 
---------------------------------------
After creating an account user will login to use the features of our website

"""

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
def bookList():
    return "Book List Page"


"""
Add
------------------------------------------------
User will add a book he want to start reading

"""
@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def addBook():
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
            # Add the book the user has selected to user_books
            db.session.execute(
                text("""
                    INSERT INTO user_books (user_id, book_id, reading_progress, completed, wishlist)
                    VALUES (:user_id, :book_id, 0, FALSE, FALSE)
                """),
                {"user_id": current_user.user_id, "book_id": book_id}
            )
            db.session.commit()
            flash("Book successfully added to your list!", category="success")

        return redirect(url_for('readingStatus'))

    return render_template('add_book.html')

"""
Search books
------------------------------------------------
Before adding a book user will search a book he wants to read

"""
@app.route('/search_books', methods=['GET'])
@login_required
def searchBooks():
    query = request.args.get('query', '').strip()

    if not query:
        return {"books": []}  # Empty response if query is empty

    # Query matching books from the database
    books = db.session.execute(
        text("SELECT book_id, book_name, writer_name FROM book_list WHERE book_name LIKE :query LIMIT 5"),
        {"query": f"%{query}%"}
    ).fetchall()

    # Convert the result into JSON format
    books_list = [{"id": book.book_id, "name": book.book_name, "writer": book.writer_name}
                   for book in books]
    return {"books": books_list}


"""
Reading Status
------------------------------------------------
In this page user can go to add book page. Also user can 
check and update the progress of books he/she is currently reading 
"""
@app.route('/reading_status')
@login_required
def readingStatus():
    # Query to fetch books the user is reading and exclude completed (100%) books
    books = db.session.execute(
        text("""
            SELECT 
                ub.user_book_id,
                b.book_name, 
                b.writer_name, 
                ub.reading_progress, 
                ub.completed
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.reading_progress < 100
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    # Convert the result into a format suitable for rendering in HTML
    user_books = [
        {
            "user_book_id": book.user_book_id,
            "book_name": book.book_name,
            "writer_name": book.writer_name,
            "reading_progress": book.reading_progress,
            "completed": book.completed
        }
        for book in books
    ]

    return render_template('reading_status.html', user_books=user_books)



"""
Save Progress
------------------------------------------------
It is a part of the Reading Status page. Here, the user 
can save the progress of his currently reading books.
"""
@app.route('/save_progress', methods=['POST'])
@login_required
def saveProgress():
    data = request.get_json()
    progresses = data.get('progresses', [])

    try:
        for progress in progresses:
            db.session.execute(
                text("""
                    UPDATE user_books
                    SET reading_progress = :progress, completed = :completed
                    WHERE user_book_id = :book_id AND user_id = :user_id
                """),
                {
                    "progress": progress['progress'],
                    "completed": progress['progress'] == '100',
                    "book_id": progress['book_id'],
                    "user_id": current_user.user_id
                }
            )
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


"""
Complete Book
------------------------------------------------
It is also a part of the Reading Status page. So, if the user clicks on save Progress 
where the progress of a book is 100 percent then the user has completed the particular book. 
As a result, it will be marked as completed in our database and we can not 
see the book in the reading progress.
"""
@app.route('/complete_book/<int:book_id>', methods=['POST'])
@login_required
def complete_book(book_id):
    # Mark the book as completed
    db.session.execute(
        text("""
            UPDATE user_books
            SET completed = TRUE, reading_progress = 100
            WHERE user_book_id = :book_id AND user_id = :user_id
        """),
        {"book_id": book_id, "user_id": current_user.user_id}
    )
    db.session.commit()
    flash("Book marked as completed!", category="success")
    return {"message": "Book marked as completed"}, 200



@app.route('/completed_books')
@login_required
def completedBooks():
    # Query to fetch completed books for the logged-in user
    completedBooks = db.session.execute(
        text("""
            SELECT 
                b.book_name, 
                b.writer_name, 
                b.genre 
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.completed = TRUE
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    # Convert the result into a format suitable for rendering in HTML
    userCompletedBooks = [
        {
            "bookName": book.book_name,
            "writerName": book.writer_name,
            "genre": book.genre,
        }
        for book in completedBooks
    ]

    return render_template('completed_books.html', completedBooks=userCompletedBooks)



from flask import request, redirect, url_for, flash

@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    if request.method == 'POST':
        # Handle adding book to wishlist
        data = request.get_json()
        bookId = data.get('book_id')
        
        if bookId:
            db.session.execute(
                text("""INSERT INTO user_books (user_id, book_id, wishlist) 
                        VALUES (:user_id, :book_id, TRUE)"""),
                {"user_id": current_user.user_id, "book_id": bookId}
            )
            db.session.commit()
            return jsonify({"status": "success"})
    
    # Fetch user's wishlist books (GET request)
    wishlistBooks = db.session.execute(
        text("""
            SELECT b.book_name, b.writer_name
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.wishlist = TRUE
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    # Convert to a list of dictionaries for easier rendering
    wishlistBooksList = [{"bookName": book.book_name, "writerName": book.writer_name}
                         for book in wishlistBooks]

    return render_template('wishlist.html', wishlistBooks=wishlistBooksList)





"""
Logout
------------------------------------------------
User can log out whenever he want
"""
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for("home"))

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)