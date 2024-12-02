Usage Instructions
==================

After setting up the application, you can use it for the following tasks:

- **Submitting a review**:
  Navigate to the `/submit_review` page, fill in the form with the book title, review text, and rating, and click **Submit**.

- **Editing a review**:
  Go to `/edit_review/{reviewId}` to update your existing review.

- **Deleting a review**:
  Navigate to `/delete_review/{reviewId}` to remove a review.

Example of a successful review submission:

```bash
POST /submit_review
{
  "book_title": "The Great Gatsby",
  "review": "A fantastic book on the American Dream.",
  "rating": 5
}
