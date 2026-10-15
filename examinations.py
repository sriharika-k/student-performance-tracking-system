
from database import connect_db


def add_subject():
    subject_name = input("Enter subject name: ").strip()

    if not subject_name:
        print("Subject name cannot be empty.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO subjects (subject_name) VALUES (?)",
            (subject_name,)
        )
        connection.commit()
        print("Subject added successfully!")

    except Exception as error:
        print("Could not add subject:", error)

    finally:
        connection.close()


def view_subjects():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT subject_id, subject_name FROM subjects ORDER BY subject_name"
    )
    subjects = cursor.fetchall()
    connection.close()

    if not subjects:
        print("No subjects found. Add a subject first.")
        return

    print("\n--- SUBJECT LIST ---")
    for subject in subjects:
        print(f"ID: {subject[0]} | Subject: {subject[1]}")


def add_marks():
    student_id = input("Enter student ID: ").strip()
    subject_id = input("Enter subject ID: ").strip()
    exam_name = input("Enter exam name: ").strip()

    if not student_id.isdigit() or not subject_id.isdigit():
        print("Student ID and subject ID must be numbers.")
        return

    if not exam_name:
        print("Exam name cannot be empty.")
        return

    try:
        marks_obtained = float(input("Enter marks obtained: "))
        max_marks = float(input("Enter maximum marks: "))
    except ValueError:
        print("Marks must be numeric.")
        return

    if max_marks <= 0:
        print("Maximum marks must be greater than zero.")
        return

    if marks_obtained < 0 or marks_obtained > max_marks:
        print("Marks must be between 0 and maximum marks.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO marks
                (student_id, subject_id, exam_name,
                 marks_obtained, max_marks)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(student_id),
                int(subject_id),
                exam_name,
                marks_obtained,
                max_marks
            )
        )
        connection.commit()
        print("Exam marks saved successfully!")

    except Exception as error:
        print("Could not save marks:", error)

    finally:
        connection.close()


def view_marks():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT s.student_id, s.name, sub.subject_name,
               m.exam_name, m.marks_obtained, m.max_marks
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        ORDER BY s.name, sub.subject_name, m.exam_name
        """
    )

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No examination records found.")
        return

    print("\n--- EXAMINATION RESULTS ---")

    for record in records:
        percentage = record[4] / record[5] * 100

        print(
            f"Student ID: {record[0]} | Name: {record[1]} | "
            f"Subject: {record[2]} | Exam: {record[3]} | "
            f"Marks: {record[4]:g}/{record[5]:g} | "
            f"Percentage: {percentage:.2f}%"
        )


def student_result():
    student_id = input("Enter student ID: ").strip()

    if not student_id.isdigit():
        print("Please enter a valid student ID.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM students WHERE student_id = ?",
        (int(student_id),)
    )
    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        connection.close()
        return

    cursor.execute(
        """
        SELECT sub.subject_name,
               SUM(m.marks_obtained),
               SUM(m.max_marks)
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE m.student_id = ?
        GROUP BY sub.subject_id, sub.subject_name
        ORDER BY sub.subject_name
        """,
        (int(student_id),)
    )

    results = cursor.fetchall()
    connection.close()

    if not results:
        print("No marks available for this student.")
        return

    print(f"\n--- RESULT: {student[0]} ---")

    total_obtained = 0
    total_maximum = 0

    for subject, obtained, maximum in results:
        percentage = obtained / maximum * 100
        total_obtained += obtained
        total_maximum += maximum

        print(
            f"{subject}: {obtained:g}/{maximum:g} "
            f"({percentage:.2f}%)"
        )

    overall_percentage = total_obtained / total_maximum * 100

    print("-" * 35)
    print(f"Total marks: {total_obtained:g}/{total_maximum:g}")
    print(f"Overall percentage: {overall_percentage:.2f}%")


def examination_menu():
    while True:
        print("\n--- EXAMINATION MANAGEMENT ---")
        print("1. Add Subject")
        print("2. View Subjects")
        print("3. Enter Exam Marks")
        print("4. View All Marks")
        print("5. View Student Result")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_subject()
        elif choice == "2":
            view_subjects()
        elif choice == "3":
            add_marks()
        elif choice == "4":
            view_marks()
        elif choice == "5":
            student_result()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    examination_menu()
