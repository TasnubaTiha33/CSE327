# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_books = db.relationship('UserBook', back_populates='user')

class Book(db.Model):
    __tablename__ = 'book_list'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=False)
    writer_name = db.Column(db.String(255), nullable=False)
    user_books = db.relationship('UserBook', back_populates='book')

class UserBook(db.Model):
    __tablename__ = 'user_books'
    user_book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book_list.book_id'))
    reading_progress = db.Column(db.String(50))  # e.g., '50%', 'Completed'
    is_removed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='user_books')
    book = db.relationship('Book', back_populates='user_books')
