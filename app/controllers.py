from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, BookList, UserBooks
from sqlalchemy.sql import text
from flask import render_template

routes = Blueprint('routes', __name__, template_folder='views')



# """
# Reading Status
# ------------------------------------------------
# In this page user can go to add book page. Also user can 
# check and update the progress of books he/she is currently reading 
# """
@routes.route('/reading_status')
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

# """
# Save Progress
# ------------------------------------------------
# It is a part of the Reading Status page. Here, the user 
# can save the progress of his currently reading books.
# """
@routes.route('/save_progress', methods=['POST'])
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

# """
# Complete Book
# ------------------------------------------------
# It is also a part of the Reading Status page. So, if the user clicks on save Progress 
# where the progress of a book is 100 percent then the user has completed the particular book. 
# As a result, it will be marked as completed in our database and we can not 
# see the book in the reading progress.
# """
@routes.route('/complete_book/<int:book_id>', methods=['POST'])
@login_required
def completeBook(book_id):
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


