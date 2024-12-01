from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import text
from your_app import db


@app.route('/user_profile')
@login_required
def user_profile():
    """Fetch and display the added, removed, and shared books for the logged-in user."""

    # Fetch added books for the logged-in user
    added_books = _get_books_by_status(current_user.user_id, is_removed=False)

    # Fetch removed books for the logged-in user
    removed_books = _get_books_by_status(current_user.user_id, is_removed=True)

    # Fetch shared books for the logged-in user
    shared_books = _get_books_by_status(current_user.user_id, is_shared=True)

    # Pass these book lists to the template
    return render_template(
        'user_profile.html',
        added_books=added_books,
        removed_books=removed_books,
        shared_books=shared_books
    )


def _get_books_by_status(user_id, is_removed=False, is_shared=False):
    """Helper function to fetch books based on the removal or sharing status."""

    query = """
        SELECT b.book_name, b.writer_name
        FROM user_books ub
        JOIN book_list b ON ub.book_id = b.book_id
        WHERE ub.user_id = :user_id
    """

    # Add conditions based on `is_removed` and `is_shared`
    if is_removed:
        query += " AND ub.is_removed = TRUE"
    if is_shared:
        query += " AND ub.is_shared = TRUE"
    if not is_removed and not is_shared:
        query += " AND ub.is_removed = FALSE"

    # Execute the query and return the result
    result = db.session.execute(text(query), {"user_id": user_id}).fetchall()
    return result
