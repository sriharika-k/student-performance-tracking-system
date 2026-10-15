
from database import connect_db


def student_performance_report():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            s.class_name,
            COALESCE(a.total_days, 0),
            COALESCE(a.present_days, 0),
            COALESCE(m.obtained, 0),
            COALESCE(m.maximum, 0)
        FROM students s
        LEFT JOIN (
            SELECT
                student_id,
                COUNT(*) AS total_days,
                SUM(
                    CASE WHEN status = 'Present'
                    THEN 1 ELSE 0 END
                ) AS present_days
            FROM attendance
            GROUP BY student_id
        ) a ON s.student_id = a.student_id
        LEFT JOIN (
            SELECT
                student_id,
                SUM(marks_obtained) AS obtained,
                SUM(max_marks) AS maximum
            FROM marks
            GROUP BY student_id
        ) m ON s.student_id = m.student_id
        ORDER BY s.name
    """)

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No student records found.")
        return

    print("\n========== STUDENT PERFORMANCE REPORT ==========")

    for record in records:
        student_id, name, class_name, total_days, present_days, obtained, maximum = record

        attendance_pct = (
            present_days / total_days * 100
            if total_days else 0
        )

        marks_pct = (
            obtained / maximum * 100
            if maximum else 0
        )

        print(f"\nStudent ID: {student_id}")
        print(f"Name: {name}")
        print(f"Class: {class_name}")

        if total_days:
            print(f"Attendance: {attendance_pct:.2f}%")
        else:
            print("Attendance: No data")

        if maximum:
            print(f"Marks Percentage: {marks_pct:.2f}%")
        else:
            print("Marks Percentage: No exam data")

        if total_days and attendance_pct < 75:
            print("Alert: Low attendance")

        if maximum and marks_pct < 40:
            print("Alert: Needs academic improvement")

        if not total_days and not maximum:
            print("Status: No attendance or exam data yet")


def top_performers():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            SUM(m.marks_obtained),
            SUM(m.max_marks)
        FROM students s
        JOIN marks m ON s.student_id = m.student_id
        GROUP BY s.student_id, s.name
        ORDER BY
            1.0 * SUM(m.marks_obtained)
            / SUM(m.max_marks) DESC,
            s.name
        LIMIT 10
    """)

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No examination data available.")
        return

    print("\n========== TOP PERFORMERS ==========")

    for rank, record in enumerate(records, start=1):
        student_id, name, obtained, maximum = record
        percentage = obtained / maximum * 100

        print(
            f"{rank}. {name} (ID: {student_id}) - "
            f"{percentage:.2f}% ({obtained:g}/{maximum:g})"
        )


def class_summary():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.class_name,
            COUNT(DISTINCT s.student_id),
            AVG(m.percentage)
        FROM students s
        LEFT JOIN (
            SELECT
                student_id,
                100.0 * SUM(marks_obtained)
                / SUM(max_marks) AS percentage
            FROM marks
            GROUP BY student_id
        ) m ON s.student_id = m.student_id
        GROUP BY s.class_name
        ORDER BY s.class_name
    """)

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No class data available.")
        return

    print("\n========== CLASS SUMMARY ==========")

    for class_name, student_count, average in records:
        average_text = (
            f"{average:.2f}%"
            if average is not None
            else "No exam data"
        )

        print(
            f"Class: {class_name} | "
            f"Students: {student_count} | "
            f"Average marks: {average_text}"
        )


def reports_menu():
    while True:
        print("\n========== PERFORMANCE REPORTS ==========")
        print("1. Student Performance Report")
        print("2. Top Performers")
        print("3. Class Summary")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            student_performance_report()
        elif choice == "2":
            top_performers()
        elif choice == "3":
            class_summary()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    reports_menu()
