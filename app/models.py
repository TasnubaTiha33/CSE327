# app/models.py

from app import db

class User(db.Model):
    """
    Represents a user in the BookVault system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username chosen by the user.
        email (str): The user's email address.
        password_hash (str): The hashed password for the user.
        created_at (datetime): The timestamp of when the user was created.
        
    Relationships:
        ratings (list of BookRating): The ratings and reviews given by the user.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    ratings = db.relationship('BookRating', back_populates='user', cascade='all, delete-orphan')


class Book(db.Model):
    """
    Represents a book in the BookVault system.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        description (str): A description of the book.
        created_at (datetime): The timestamp of when the book was added to the system.
        
    Relationships:
        ratings (list of BookRating): The ratings and reviews for this book.
    """

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    ratings = db.relationship('BookRating', back_populates='book', cascade='all, delete-orphan')


class BookRating(db.Model):
    """
    Represents a rating and review for a specific book by a user.

    Attributes:
        id (int): The unique identifier for the rating.
        user_id (int): The ID of the user who gave the rating.
        book_id (int): The ID of the book that was rated.
        rating (int): The rating given by the user (usually 1 to 5).
        review (str): The review text provided by the user (optional).
        created_at (datetime): The timestamp when the rating was created.

    Relationships:
        user (User): The user who gave the rating.
        book (Book): The book that was rated.
    """

    __tablename__ = 'book_ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='ratings')
    book = db.relationship('Book', back_populates='ratings')



