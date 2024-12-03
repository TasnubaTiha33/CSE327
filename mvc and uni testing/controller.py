from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text
from . import db
from .models import UserBooks, BookList

@app.route('/user_profile')
@login_required
def user_profile():
    # Query for user books and their reading progress
    query = """
        SELECT b.book_name, b.writer_name, ub.reading_progress
        FROM user_books ub
        JOIN book_list b ON ub.book_id = b.book_id
        WHERE ub.user_id = :user_id AND ub.is_removed = FALSE
    """
    # Execute the query with the user_id of the logged-in user
    result = db.session.execute(text(query), {'user_id': current_user.id}).fetchall()

    # Format the result into a list of dictionaries
    books = [{"book_name": row[0], "writer_name": row[1], "reading_progress": row[2]} for row in result]

    # If no books, you can flash a message or handle the case
    if not books:
        flash('You have no books in progress.', 'info')

    # Render the template and pass the books data to the view
    return render_template('user_profile.html', books=books)
