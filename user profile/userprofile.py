@app.route('/user_profile')
@login_required
def userProfile():
    # Fetch added, removed, and shared books for the logged-in user
    added_books = db.session.execute(
        text("""
            SELECT b.book_name, b.writer_name, ub.reading_progress
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.is_removed = FALSE
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    removed_books = db.session.execute(
        text("""
            SELECT b.book_name, b.writer_name
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.is_removed = TRUE
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    shared_books = db.session.execute(
        text("""
            SELECT b.book_name, b.writer_name
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.is_shared = TRUE
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    # Pass these book lists to the template
    return render_template('user_profile.html', 
                           added_books=added_books, 
                           removed_books=removed_books, 
                           shared_books=shared_books)
