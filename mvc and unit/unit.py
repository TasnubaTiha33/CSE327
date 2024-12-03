import unittest
from your_app import create_app, db
from flask_login import login_user
from your_app.models import User, BookList, UserBooks  # Assuming these models exist

class UserProfileTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')  # Use a testing config
        self.client = self.app.test_client()
        
        # Create a user in the test database
        self.user = User(username='testuser', password='testpassword')
        db.session.add(self.user)
        db.session.commit()

        # Log the user in for the tests
        login_user(self.user)

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()

    def test_user_profile_route(self):
        """Test the user profile route."""
        response = self.client.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser', response.data)
        self.assertIn(b'Added Books', response.data)

    def test_added_books(self):
        """Test if added books show up correctly."""
        # Create a test book and associate it with the user
        book = BookList(book_name="Test Book", writer_name="Test Author")
        db.session.add(book)
        db.session.commit()

        user_book = UserBooks(user_id=self.user.id, book_id=book.book_id, reading_progress=50, is_removed=False)
        db.session.add(user_book)
        db.session.commit()

        # Check if the book appears in the profile
        response = self.client.get('/user_profile')
        self.assertIn(b'Test Book', response.data)
        self.assertIn(b'50', response.data)  # Reading progress should show up

if __name__ == '__main__':
    unittest.main()
