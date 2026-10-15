
from database import connect_db
from datetime import date


def mark_attendance():
    student_id = input("Enter student ID: ").strip()

    if not student_id.isdigit():
        print("Invalid student ID.")
        return

    attendance_date = input(
        "Enter date (YYYY-MM-DD), or press Enter for today: "
    ).strip()

    if not attendance_date:
        attendance_date = date.today().isoformat()

    try:
        date.fromisoformat(attendance_date)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    status = input("Enter status (Present/Absent): ").strip().title()

    if status not in ("Present", "Absent"):
        print("Status must be Present or Absent.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO attendance
                (student_id, attendance_date, status)
            VALUES (?, ?, ?)
            """,
            (int(student_id), attendance_date, status)
        )
        connection.commit()
        print("Attendance recorded successfully!")

    except Exception as error:
        print("Could not record attendance:", error)

    finally:
        connection.close()


def view_attendance():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT s.student_id, s.name,
               a.attendance_date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        ORDER BY a.attendance_date DESC, s.name
        """
    )

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No attendance records found.")
        return

    print("\n--- ATTENDANCE RECORDS ---")

    for record in records:
        print(
            f"ID: {record[0]} | Name: {record[1]} | "
            f"Date: {record[2]} | Status: {record[3]}"
        )


def attendance_percentage():
    student_id = input("Enter student ID: ").strip()

    if not student_id.isdigit():
        print("Invalid student ID.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM students
        WHERE student_id = ?
        """,
        (int(student_id),)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        connection.close()
        return

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_days,
            SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END)
        FROM attendance
        WHERE student_id = ?
        """,
        (int(student_id),)
    )

    total_days, present_days = cursor.fetchone()
    connection.close()

    if total_days == 0:
        print("No attendance records available for this student.")
        return

    percentage = (present_days / total_days) * 100

    print(f"\nStudent: {student[0]}")
    print(f"Total attendance entries: {total_days}")
    print(f"Days present: {present_days}")
    print(f"Attendance percentage: {percentage:.2f}%")

    if percentage < 75:
        print("Warning: Attendance is below 75%.")
    else:
        print("Attendance is satisfactory.")


def attendance_menu():
    while True:
        print("\n--- ATTENDANCE MANAGEMENT ---")
        print("1. Mark Attendance")
        print("2. View Attendance Records")
        print("3. Calculate Attendance Percentage")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            attendance_percentage()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    attendance_menu()
