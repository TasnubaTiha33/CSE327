from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.user_id)

class BookList(db.Model):
    __tablename__ = 'book_list'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), unique=True, nullable=False)
    writer_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=True)

class UserBooks(db.Model):
    __tablename__ = 'user_books'
    user_book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_list.book_id'), nullable=False)
    reading_progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    review = db.Column(db.Text, nullable=True)
    user_rating = db.Column(db.Integer, nullable=True)
