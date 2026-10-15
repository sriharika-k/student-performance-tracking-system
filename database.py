
import sqlite3


def connect_db():
    connection = sqlite3.connect("student_performance.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL
                CHECK (status IN ('Present', 'Absent')),
            UNIQUE (student_id, attendance_date),
            FOREIGN KEY (student_id)
                REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            exam_name TEXT NOT NULL,
            marks_obtained REAL NOT NULL
                CHECK (marks_obtained >= 0),
            max_marks REAL NOT NULL
                CHECK (max_marks > 0),
            CHECK (marks_obtained <= max_marks),
            FOREIGN KEY (student_id)
                REFERENCES students(student_id),
            FOREIGN KEY (subject_id)
                REFERENCES subjects(subject_id),
            UNIQUE (student_id, subject_id, exam_name)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


if __name__ == "__main__":
    create_tables()
