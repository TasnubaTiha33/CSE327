# test_query.py
from app import create_app, db
from app.models import Book

# Create Flask app context
app = create_app()

# Use Flask app context to run queries
with app.app_context():
    # Query all books
    books = Book.query.all()
    
    # Print out the titles of the books
    for book in books:
        print(book.title)
