import pytest
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from unittest.mock import patch

# Assuming the Flask app is named 'app' and db is initialized as 'db'
from app import app, db, User, Book, UserBooks

@pytest.fixture
def client():
    # Set up the Flask test client and mock the necessary database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()

    with app.test_client() as client:
        yield client

    db.drop_all()

@pytest.fixture
def mock_user():
    # Mock a user object with an example user_id
    user = User(user_id=1, username='testuser', email='testuser@example.com', password='password')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def mock_books():
    # Add mock books to the book list table for the test
    book1 = Book(book_id=1, book_name='Book One', writer_name='Author One')
    book2 = Book(book_id=2, book_name='Book Two', writer_name='Author Two')
    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()

def test_wishlist_get(client, mock_user, mock_books):
    # Mock the user being logged in
    with patch('flask_login.current_user', mock_user):
        # Simulate a GET request to fetch the wishlist
        response = client.get('/wishlist')
        
        # Check if the response contains the book names
        assert response.status_code == 200
        assert 'Book One' in response.data.decode()
        assert 'Book Two' in response.data.decode()

def test_wishlist_post(client, mock_user, mock_books):
    # Mock the user being logged in and sending a POST request with book_id
    with patch('flask_login.current_user', mock_user):
        data = {'book_id': 1}
        response = client.post('/wishlist', json=data)

        # Check if the book was added successfully
        assert response.status_code == 200
        assert response.json['status'] == 'success'

        # Verify that the book has been added to the user's wishlist in the database
        user_books = db.session.execute(
            """SELECT * FROM user_books WHERE user_id = :user_id AND wishlist = TRUE""",
            {"user_id": mock_user.user_id}
        ).fetchall()
        assert len(user_books) == 1
        assert user_books[0].book_id == 1

def test_wishlist_post_missing_book_id(client, mock_user, mock_books):
    # Simulate a POST request without a book_id
    with patch('flask_login.current_user', mock_user):
        data = {}
        response = client.post('/wishlist', json=data)
        
        # Check that the response is an error because book_id is missing
        assert response.status_code == 400
        assert 'error' in response.json
