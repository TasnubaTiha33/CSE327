from flask import Flask, render_template, request, redirect, url_for, flash, session
import models

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Configure the database connection
app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'MyNewPassword123'
app.config['DB_NAME'] = 'review'


@app.route('/submit_review', methods=['GET', 'POST'])
def submitReview():
    """
    Display and handle the review submission form.

    This route renders the review submission form when accessed via GET request. 
    If the user is logged in and submits the form via a POST request, 
    it validates the data and adds the review to the database.

    If the user is not logged in, they are redirected to the login page.

    Methods:
        GET: Renders the review submission form.
        POST: Handles form submission, validates input, and adds the review to the database.

    Returns:
        Redirect: Redirects to the same page after the form is submitted or when an error occurs.
    """
    if 'logged_in' not in session:
        flash("Please log in to submit a review.", "error")
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    if request.method == 'POST':
        bookTitle = request.form['book_title']
        reviewerName = session['username']  # Assume user's name is in session
        review = request.form['review']
        rating = int(request.form['rating'])
        
        message = models.addReview(bookTitle, reviewerName, review, rating)
        flash(message, "success" if "Thanks" in message else "error")
        return redirect(url_for('submitReview'))
        
    return render_template('review_form.html')


@app.route('/edit_review/<int:reviewId>', methods=['GET', 'POST'])
def editReview(reviewId):
    """
    Allow users to edit their existing review.

    This route renders the review editing form when accessed via GET request 
    with a review ID. When the user submits the form, it updates the review 
    in the database.

    If the user is not logged in, they are redirected to the login page.

    Methods:
        GET: Fetches the review data and displays the edit form.
        POST: Updates the review in the database and redirects back to the review submission page.

    Parameters:
        reviewId (int): The ID of the review to be edited.

    Returns:
        Redirect: Redirects to the review submission page after a successful update.
    """
    if 'logged_in' not in session:
        flash("Please log in to edit a review.", "error")
        return redirect(url_for('login'))
    
    # Fetch the review to be edited
    review = models.getReviewById(reviewId)  # You need to implement this method
    
    if request.method == 'POST':
        updatedReview = request.form['review']
        updatedRating = int(request.form['rating'])
        
        message = models.updateReview(reviewId, updatedReview, updatedRating)
        flash(message, "success" if "updated" in message else "error")
        return redirect(url_for('submitReview'))
    
    return render_template('edit_review_form.html', reviewId=reviewId, review=review)


@app.route('/delete_review/<int:reviewId>', methods=['POST'])
def deleteReview(reviewId):
    """
    Allow users to delete a review.

    This route deletes a review from the database based on the provided review ID.

    If the user is not logged in, they are redirected to the login page.

    Methods:
        POST: Deletes the review from the database.

    Parameters:
        reviewId (int): The ID of the review to be deleted.

    Returns:
        Redirect: Redirects to the review submission page after the review is deleted.
    """
    if 'logged_in' not in session:
        flash("Please log in to delete a review.", "error")
        return redirect(url_for('login'))
    
    message = models.deleteReview(reviewId)
    flash(message, "success" if "removed" in message else "error")
    return redirect(url_for('submitReview'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    This route renders the login form when accessed via GET request. 
    If the user submits the form via POST request, it checks the credentials, 
    and if they are valid, it logs the user in and redirects them to the review submission page.
    
    If the credentials are incorrect, an error message is displayed.

    Methods:
        GET: Renders the login form.
        POST: Verifies user credentials and logs the user in.

    Returns:
        Redirect: Redirects to the review submission page if login is successful.
        Template: Renders the login page if login fails or during the initial GET request.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Assume password is verified here
        
        # Updated login check
        if username == 'Tasnuba12' and password == 'Rosett12':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('submitReview'))
        else:
            flash("Invalid credentials.", "error")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Logout the user.

    This route logs the user out by clearing the session variables and redirects
    them to the login page with a success message.

    Methods:
        GET: Logs the user out and redirects to the login page.

    Returns:
        Redirect: Redirects to the login page after logging out.
    """
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You have logged out.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
