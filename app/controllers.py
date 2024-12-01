from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Book, BookRating
from app import db

bp = Blueprint('controllers', __name__)

@bp.route('/')
def index():
    """
    Renders the index page displaying a list of all books in the system.

    This route fetches all the books from the database and renders them in
    the `index.html` template.

    Returns:
        Response: The rendered HTML page displaying the list of books.
    """
    books = Book.query.all()
    return render_template('index.html', books=books)

@bp.route('/rate/<int:book_id>', methods=['GET', 'POST'])
def rate_book(book_id):
    """
    Allows users to rate a specific book and submit a review.

    This route handles both GET and POST requests for the rating system. On 
    GET requests, it displays the rating form for the specified book. On 
    POST requests, it processes the form data, saves the rating and review 
    to the database, and redirects the user back to the book's rating page.

    Parameters:
        book_id (int): The ID of the book to be rated.

    Returns:
        Response: Redirects to the book rating page upon successful submission.
                Otherwise, renders the rating form for the book.
    """
    # Query the book by its ID
    book = Book.query.get_or_404(book_id)

    # If the form is submitted (POST request), handle the rating logic here
    if request.method == 'POST':
        rating = request.form['rating']
        review = request.form['review']
        
        # Assuming User is logged in, we'd use current_user to get the logged-in user
        # For now, we'll use a dummy user with ID 1
        user_id = 1  # Replace with actual user logic
        
        # Save the rating to the database
        book_rating = BookRating(user_id=user_id, book_id=book.id, rating=rating, review=review)
        db.session.add(book_rating)
        db.session.commit()

        # Flash a success message
        flash('Your rating and review have been submitted successfully!', 'success')

        # Redirect to the same page or a new page after form submission
        return redirect(url_for('controllers.rate_book', book_id=book.id))
    
    # Render the template and pass the book object
    return render_template('rate_book.html', book=book)



