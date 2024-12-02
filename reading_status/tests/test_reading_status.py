import pytest
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect(":memory:")  # Use in-memory database for testing
    cursor = conn.cursor()
    
    # Create Users and Books tables
    cursor.execute("""
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookname TEXT UNIQUE
        )
    """)
    
    # Insert sample data
    users = [("testuser1",), ("testuser2",), ("testuser3",)]
    books = [
        ("The Catcher in the Rye",),
        ("To Kill a Mockingbird",),
        ("1984",),
        ("Moby Dick",),
        ("Pride and Prejudice",)
    ]
    cursor.executemany("INSERT INTO Users (username) VALUES (?)", users)
    cursor.executemany("INSERT INTO Books (bookname) VALUES (?)", books)
    conn.commit()
    
    return conn

# Function to validate reading progress using the database
def validate_reading_progress_with_db(conn, username, bookname, progress):
    # Validate progress
    if not (0 <= progress <= 100):
        return False

    # Check username and bookname in the database
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    user_exists = cursor.fetchone() is not None
    cursor.execute("SELECT 1 FROM Books WHERE bookname = ?", (bookname,))
    book_exists = cursor.fetchone() is not None
    
    return user_exists and book_exists

# Test cases with database
@pytest.fixture
def database():
    conn = setup_database()
    yield conn
    conn.close()

@pytest.mark.parametrize(
    "username, bookname, progress, expected",
    [
        # Valid test cases
        ("testuser1", "The Catcher in the Rye", 50, True),
        ("testuser2", "1984", 0, True),
        ("testuser3", "Moby Dick", 100, True),

        # Invalid progress test cases
        ("testuser1", "The Catcher in the Rye", -10, False),
        ("testuser2", "1984", 120, False), 

        # Invalid username or bookname
        ("unknownuser", "The Catcher in the Rye", 50, False), 
        ("testuser1", "Unknown Book", 50, False),             
    ]
)
def test_reading_progress_with_db(database, username, bookname, progress, expected):
    result = validate_reading_progress_with_db(database, username, bookname, progress)
    assert result == expected
