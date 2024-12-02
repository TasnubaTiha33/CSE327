from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .model import db, BookList, UserBooks
from sqlalchemy.sql import text

# Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/completed_books')
@login_required
def completed_books():
    # Query to fetch completed books for the logged-in user
    completed_books = db.session.execute(
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

    # Convert to a format suitable for rendering
    user_completed_books = [
        {
            "bookName": book.book_name,
            "writerName": book.writer_name,
            "genre": book.genre,
        }
        for book in completed_books
    ]

    return render_template('completed_books.html', completedBooks=user_completed_books)
