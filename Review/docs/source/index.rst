Welcome to Your Project's Documentation!
========================================

This is the main page of the documentation for your project. Here you can include general information about your project, its purpose, and how to get started.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   setup
   usage
   api
   models  # Add this line to link to your models documentation

Models Documentation
====================

The following functions are part of the `models.py` module for handling book reviews.

1. **getDbConnection** - Establishes a connection to the MySQL database using the Flask app's configuration.
2. **addReview** - Adds a new book review to the database after validating the review's length.
3. **getReviewById** - Fetches a review from the database by its ID.
4. **updateReview** - Updates an existing review after validating the review's length.
5. **deleteReview** - Deletes a review from the database by its ID.

Source Code
------------
Here is the source code for the above functions:

.. code-block:: python
   :linenos:

   import mysql.connector
   from flask import current_app

   def getDbConnection():
       """
       Establishes a connection to the database using configuration values from the Flask app.
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
       Updates an existing review after validating the review's length.
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
       """
       connection = getDbConnection()
       cursor = connection.cursor()
       cursor.execute("DELETE FROM reviews WHERE id = %s", (reviewId,))
       connection.commit()
       cursor.close()
       connection.close()
       return "Your review has been removed"
