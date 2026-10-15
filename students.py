
from database import connect_db


def add_student():
    name = input("Enter student name: ").strip()
    class_name = input("Enter class name: ").strip()
    email = input("Enter email (or leave blank): ").strip()

    if not name or not class_name:
        print("Name and class are required.")
        return

    if not email:
        email = None

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, class_name, email)
            VALUES (?, ?, ?)
            """,
            (name, class_name, email)
        )
        connection.commit()
        print("Student added successfully!")

    except Exception as error:
        print("Could not add student:", error)

    finally:
        connection.close()


def view_students():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT student_id, name, class_name, email FROM students"
    )
    students = cursor.fetchall()
    connection.close()

    if not students:
        print("No students found.")
        return

    print("\n--- STUDENT LIST ---")
    for student in students:
        print(
            f"ID: {student[0]} | Name: {student[1]} | "
            f"Class: {student[2]} | Email: {student[3] or 'N/A'}"
        )


def search_student():
    student_id = input("Enter student ID: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid numeric student ID.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_id, name, class_name, email
        FROM students
        WHERE student_id = ?
        """,
        (int(student_id),)
    )
    student = cursor.fetchone()
    connection.close()

    if student:
        print("\nStudent found:")
        print(f"ID: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Class: {student[2]}")
        print(f"Email: {student[3] or 'N/A'}")
    else:
        print("Student not found.")


def update_student():
    student_id = input("Enter student ID to update: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid numeric student ID.")
        return

    name = input("Enter new name: ").strip()
    class_name = input("Enter new class: ").strip()
    email = input("Enter new email (or leave blank): ").strip()

    if not name or not class_name:
        print("Name and class are required.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE students
            SET name = ?, class_name = ?, email = ?
            WHERE student_id = ?
            """,
            (name, class_name, email or None, int(student_id))
        )
        connection.commit()

        if cursor.rowcount:
            print("Student updated successfully!")
        else:
            print("Student ID not found.")

    except Exception as error:
        print("Could not update student:", error)

    finally:
        connection.close()


def delete_student():
    student_id = input("Enter student ID to delete: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid numeric student ID.")
        return

    confirm = input("Are you sure? Type YES to delete: ").strip()

    if confirm != "YES":
        print("Deletion cancelled.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (int(student_id),)
        )
        connection.commit()

        if cursor.rowcount:
            print("Student deleted successfully!")
        else:
            print("Student ID not found.")

    except Exception as error:
        print("Could not delete student:", error)

    finally:
        connection.close()


def student_menu():
    while True:
        print("\n--- STUDENT MANAGEMENT ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")
