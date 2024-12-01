@app.route('/user_profile')
@login_required
def userProfile():
    added_books = db.session.execute(
        text("""
            SELECT b.book_name, b.writer_name, ub.reading_progress
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            WHERE ub.user_id = :user_id AND ub.is_removed = FALSE
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    shared_books = db.session.execute(
        text("""
            SELECT b.book_name, b.writer_name, u.username
            FROM user_books ub
            JOIN book_list b ON ub.book_id = b.book_id
            JOIN users u ON ub.shared_with_user_id = u.user_id
            WHERE ub.user_id = :user_id AND ub.shared_with_user_id IS NOT NULL
        """),
        {"user_id": current_user.user_id}
    ).fetchall()

    return render_template('user_profile.html', added_books=added_books, shared_books=shared_books)
