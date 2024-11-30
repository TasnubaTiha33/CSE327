import pytest
from app import create_app, db
from app.models import User, Book, BookRating

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MyNewPassword123@localhost/rating'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create tables in the test database
    yield app
    with app.app_context():
        db.drop_all()  # Drop tables after the test

@pytest.fixture
def add_sample_data(app):
    # Add some sample books and users
    with app.app_context():
        book1 = Book(title='The Catcher in the Rye', author='J.D. Salinger', description='A novel about Holden Caulfield.')
        user1 = User(username='testuser', email='test@example.com', password_hash='hashedpassword123')
        db.session.add(book1)
        db.session.add(user1)
        db.session.commit()
    yield
    # Cleanup data after tests
    with app.app_context():
        db.session.remove()

def test_book_insertion(app, add_sample_data):
    with app.app_context():
        # Check if the book is inserted
        book = Book.query.filter_by(title='The Catcher in the Rye').first()
        assert book is not None
        assert book.title == 'The Catcher in the Rye'

def test_user_insertion(app, add_sample_data):
    with app.app_context():
        # Check if the user is inserted
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'

def test_rating_submission(app, add_sample_data):
    with app.app_context():
        # Add a rating
        user = User.query.filter_by(username='testuser').first()
        book = Book.query.filter_by(title='The Catcher in the Rye').first()
        rating = BookRating(user_id=user.id, book_id=book.id, rating=5, review='Masterpiece')
        db.session.add(rating)
        db.session.commit()

        # Check if the rating is correctly inserted
        rating_in_db = BookRating.query.filter_by(user_id=user.id, book_id=book.id).first()
        assert rating_in_db is not None
        assert rating_in_db.rating == 5
        assert rating_in_db.review == 'Masterpiece'
