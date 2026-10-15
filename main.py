from examinations import examination_menu
from database import create_tables
from students import student_menu
from attendance import attendance_menu
from reports import reports_menu


def main():
    # Create the database tables
    create_tables()

    while True:
        print("\n==========================================")
        print("   STUDENT PERFORMANCE TRACKING SYSTEM")
        print("==========================================")
        print("1. Student Management")
        print("2. Attendance Management")
        print("3. Examination Management")
        print("4. Performance Reports")
        print("5. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            student_menu()

        elif choice == "2":
            attendance_menu()

        elif choice == "3":
            examination_menu()
        elif choice == "4":
              reports_menu()

        elif choice == "5":
            print("\nThank you for using the system!")
            print("Application closed successfully.")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
