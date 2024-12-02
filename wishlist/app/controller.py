from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .model import db, UserBooks
from sqlalchemy.sql import text

# Create the blueprint for the wishlist
wishlist_bp = Blueprint('wishlist', __name__)

# Route for the wishlist page
@wishlist_bp.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    if request.method == 'POST':
        # Handle adding book to wishlist
        data = request.get_json()
        book_id = data.get('book_id')

        if book_id:
            existing_entry = UserBooks.query.filter_by(user_id=current_user.user_id, book_id=book_id).first()
            if not existing_entry:
                new_entry = UserBooks(user_id=current_user.user_id, book_id=book_id, wishlist=True)
                db.session.add(new_entry)
                db.session.commit()
                return jsonify({"status": "success"})

        return jsonify({"status": "error", "message": "Failed to add book"})

    # Fetch user's wishlist books (GET request)
    wishlist_books = db.session.execute(
        """
        SELECT b.book_name, b.writer_name
        FROM user_books ub
        JOIN book_list b ON ub.book_id = b.book_id
        WHERE ub.user_id = :user_id AND ub.wishlist = TRUE
        """, {"user_id": current_user.user_id}
    ).fetchall()

    wishlist_books_list = [{"bookName": book.book_name, "writerName": book.writer_name} for book in wishlist_books]
    
    return render_template('wishlist.html', wishlistBooks=wishlist_books_list)

# Route for removing a book from the wishlist
@wishlist_bp.route('/remove_from_wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    data = request.get_json()
    book_id = data.get('book_id')

    if book_id:
        entry = UserBooks.query.filter_by(user_id=current_user.user_id, book_id=book_id, wishlist=True).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({"status": "success"})
    
    return jsonify({"status": "error", "message": "Failed to remove book"})
