from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, BookList, UserBooks
from sqlalchemy.sql import text
from flask import render_template

routes = Blueprint('routes', __name__, template_folder='views')

# """
# Add
# ------------------------------------------------
# User will add a book he want to start reading

# """
@routes.route('/add_book', methods=['GET', 'POST'])
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

# """
# Search books
# ------------------------------------------------
# Before adding a book user will search a book he wants to read

# """
@routes.route('/search_books', methods=['GET'])
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
