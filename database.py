import sqlite3

DATABASE_NAME = "academic.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """Create the required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # Student information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            semester INTEGER NOT NULL,
            branch TEXT NOT NULL
        )
    """)

    # Subject information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT UNIQUE NOT NULL,
            max_marks INTEGER NOT NULL DEFAULT 100
        )
    """)

    # Marks information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            marks REAL NOT NULL,
            UNIQUE(student_id, subject_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    """)

    connection.commit()
    connection.close()

    add_default_subjects()


def add_default_subjects():
    """Add initial subjects if they are not already present."""

    connection = get_connection()
    cursor = connection.cursor()

    subjects = [
        ("CSE101", "Programming"),
        ("MAT101", "Calculus"),
        ("ENG101", "English"),
        ("EVS101", "Environmental Studies")
    ]

    for code, name in subjects:
        cursor.execute("""
            INSERT OR IGNORE INTO subjects
            (subject_code, subject_name, max_marks)
            VALUES (?, ?, 100)
        """, (code, name))

    connection.commit()
    connection.close()


def get_subjects():
    """Return all subjects stored in the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject_id, subject_code, subject_name, max_marks
        FROM subjects
        ORDER BY subject_id
    """)

    subjects = cursor.fetchall()
    connection.close()

    return subjects