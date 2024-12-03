# test_user_profile.py
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, User, Book, UserBook
from flask_login import login_user

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        # Set up the Flask app and test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.client = app.test_client()
        db.create_all()

        # Create test data
        self.user = User(username='testuser')
        self.book = Book(book_name='Test Book', writer_name='Test Writer')
        self.user_book = UserBook(user=self.user, book=self.book, reading_progress='50%', is_removed=False)
        
        db.session.add(self.user)
        db.session.add(self.book)
        db.session.add(self.user_book)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_profile(self):
        # Log in the user
        login_user(self.user)

        # Simulate a GET request to the /user_profile route
        response = self.client.get('/user_profile')

        # Check if the page contains the book name and progress
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)
        self.assertIn(b'Progress: 50%', response.data)

if __name__ == '__main__':
    unittest.main()
