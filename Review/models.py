import mysql.connector
from flask import current_app

def getDbConnection():
    """
    Establishes a connection to the database using configuration values from the Flask app.

    This function uses the Flask `current_app` context to fetch database connection details
    (such as host, user, password, and database) from the app's config. It returns a 
    MySQL connection object that can be used for executing queries.

    Returns:
        connection (mysql.connector.connection.MySQLConnection): A connection to the database.

    Raises:
        mysql.connector.errors.ProgrammingError: If the database connection fails.
    """
    connection = mysql.connector.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_NAME']
    )
    return connection


def addReview(bookTitle, reviewerName, review, rating):
    """
    Adds a new book review to the database after validating the review's length.

    This function inserts a new review into the `reviews` table. It checks if the review 
    exceeds a maximum length (1000 words), and if so, returns an error message. If the 
    review passes validation, it inserts the review into the database.

    Args:
        bookTitle (str): The title of the book being reviewed.
        reviewerName (str): The name of the person submitting the review.
        review (str): The text content of the review.
        rating (int): The rating given to the book (usually between 1 and 5).

    Returns:
        str: A message indicating the result of the operation, either success or failure.

    Raises:
        mysql.connector.errors.InterfaceError: If the database connection fails.
        mysql.connector.errors.ProgrammingError: If the SQL query is invalid.
    """
    if len(review.split()) > 1000:
        return "Review too long"
    
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO reviews (book_title, reviewer_name, review, rating) VALUES (%s, %s, %s, %s)",
        (bookTitle, reviewerName, review, rating)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return "Thanks for your review!"


def getReviewById(reviewId):
    """
    Fetches a review from the database by its ID.

    This function retrieves a review from the `reviews` table based on the given review ID.
    If the review exists, it returns a dictionary containing the review's details. Otherwise, 
    it returns None.

    Args:
        reviewId (int): The unique identifier of the review to fetch.

    Returns:
        dict or None: A dictionary containing the review details (id, book_title, review, rating),
                      or None if the review does not exist.

    Raises:
        mysql.connector.errors.InterfaceError: If the database connection fails.
        mysql.connector.errors.ProgrammingError: If the SQL query is invalid.
    """
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reviews WHERE id = %s", (reviewId,))
    review = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if review:
        return {
            'id': review[0],
            'book_title': review[1],
            'review': review[2],
            'rating': review[3]
        }
    return None


def updateReview(reviewId, review):
    """
    Updates an existing review in the database after validating the review's length.

    This function updates an existing review in the `reviews` table. It checks if the new review 
    text exceeds a maximum length (1000 words), and if so, returns an error message. If the review 
    passes validation, it updates the review in the database.

    Args:
        reviewId (int): The unique identifier of the review to update.
        review (str): The updated review text.

    Returns:
        str: A message indicating the result of the operation, either success or failure.

    Raises:
        mysql.connector.errors.InterfaceError: If the database connection fails.
        mysql.connector.errors.ProgrammingError: If the SQL query is invalid.
    """
    if len(review.split()) > 1000:
        return "Review too long"
    
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE reviews SET review = %s WHERE id = %s",
        (review, reviewId)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return "Your review has been updated"


def deleteReview(reviewId):
    """
    Deletes a review from the database by its ID.

    This function removes a review from the `reviews` table based on the given review ID.
    It performs a DELETE operation on the database and commits the change.

    Args:
        reviewId (int): The unique identifier of the review to delete.

    Returns:
        str: A message indicating the result of the operation, either success or failure.

    Raises:
        mysql.connector.errors.InterfaceError: If the database connection fails.
        mysql.connector.errors.ProgrammingError: If the SQL query is invalid.
    """
    connection = getDbConnection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = %s", (reviewId,))
    connection.commit()
    cursor.close()
    connection.close()
    return "Your review has been removed"
