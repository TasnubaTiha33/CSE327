import pytest
import sys
import os

# Ensure we can import the app directly from app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import directly from app.py

# Fixture to set up the app for testing
@pytest.fixture
def testClient():
    """Fixture to set up the app for testing with a test-specific database."""
    # Use a test-specific database to prevent changes to the production database
    app.config['TESTING'] = True
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_USER'] = 'root'
    app.config['DB_PASSWORD'] = 'MyNewPassword123'
    app.config['DB_NAME'] = 'test_db'  # Use a test database
    app.config['SECRET_KEY'] = 'testsecretkey'  # For session management in tests
    
    with app.test_client() as client:
        with app.app_context():
            # Set up the database schema for testing (if needed)
            # This would be where you set up any test data or schema (skip if done elsewhere)
            yield client
            # Cleanup: Optionally clear out the database after the test is done
            # You can add code here to remove test data if necessary.

# Test: Home page loads correctly
def testHome(testClient):
    """Test if the review submission form page loads."""
    response = testClient.get('/submit_review')
    assert response.status_code == 200  # Check if the page loaded successfully
    assert b'Submit Your Book Review' in response.data  # Check if the page contains the expected title

# Test: Login page loads and handles login
def testLoginPage(testClient):
    """Test login page rendering and login form."""
    response = testClient.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data  # Check if login page is loaded

# Test: Submitting a review
def testSubmitReview(testClient):
    """Test the review submission form."""
    # Simulate a login session
    with testClient.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'Tasnuba12'

    # Submit a review via POST
    response = testClient.post('/submit_review', data={
        'book_title': 'Test Book',
        'review': 'This is a test review.',
        'rating': 5
    })

    assert response.status_code == 302  # Check for redirect after submitting review
    assert b'Thanks for your review!' in response.data  # Check for success message

# Test: Edit an existing review
def testEditReview(testClient):
    """Test editing an existing review."""
    # Simulate a login session
    with testClient.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'Tasnuba12'

    # Assume reviewId=1 (you may want to replace it with an actual review from your test DB)
    reviewId = 1

    # Get the review form with current review details
    response = testClient.get(f'/edit_review/{reviewId}')
    assert response.status_code == 200
    assert b'Edit Your Review' in response.data  # Ensure form loads

    # Update review via POST
    response = testClient.post(f'/edit_review/{reviewId}', data={
        'review': 'Updated review content.',
        'rating': 4
    })

    assert response.status_code == 302  # Check for redirect after update
    assert b'Your review has been updated' in response.data  # Success message

# Test: Delete a review
def testDeleteReview(testClient):
    """Test deleting an existing review."""
    # Simulate a login session
    with testClient.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'Tasnuba12'

    # Assume reviewId=1 (replace with actual ID)
    reviewId = 1

    # Delete review via POST
    response = testClient.post(f'/delete_review/{reviewId}')
    assert response.status_code == 302  # Check for redirect after deletion
    assert b'Your review has been removed' in response.data  # Check for success message

# Test: Logout functionality
def testLogout(testClient):
    """Test the logout functionality."""
    with testClient.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = 'Tasnuba12'

    # Trigger logout
    response = testClient.get('/logout')

    # Check for the redirect status code
    assert response.status_code == 302

    # Check for the redirect location (the login page)
    assert response.location == 'http://localhost/login'
