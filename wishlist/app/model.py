from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
from .model import UserBooks, Book, User
from flask_login import UserMixin


# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relationship with Book through the UserBooks association table
    books = db.relationship('Book', secondary='user_books', backref='users')

# Book model
class Book(db.Model):
    __tablename__ = 'book_list'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    writer_name = db.Column(db.String(200), nullable=False)
    
    # Relationship with User through the UserBooks association table
    users = db.relationship('User', secondary='user_books', backref='books')

# User-Book association table for wishlist
class UserBooks(db.Model):
    __tablename__ = 'user_books'
    user_books_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_list.book_id'), nullable=False)
    wishlist = db.Column(db.Boolean, default=True)

# Blueprint for wishlist routes
wishlist_bp = Blueprint('wishlist', __name__)

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
