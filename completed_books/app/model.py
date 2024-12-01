from . import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class BookList(db.Model):
    __tablename__ = 'book_list'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(150), nullable=False)
    writer_name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=True)

class UserBooks(db.Model):
    __tablename__ = 'user_books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_list.book_id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    wishlist = db.Column(db.Boolean, default=False)
