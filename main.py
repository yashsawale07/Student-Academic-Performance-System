from student import (
    add_student,
    search_student,
    view_all_students,
    update_student,
    delete_student
)

from marks import (
    add_marks,
    view_marks,
    update_marks
)

from result import show_result
from analysis import show_analysis
from report import generate_report
from dashboard import show_dashboard
from database import initialize_database


def student_management():
    while True:
        print("\n" + "=" * 45)
        print("           STUDENT MANAGEMENT")
        print("=" * 45)

        print("1. Add Student")
        print("2. Search Student")
        print("3. View All Students")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            search_student()

        elif choice == "3":
            view_all_students()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            break

        else:
            print("\n❌ Invalid choice. Please enter 1-6.")


def marks_management():
    while True:
        print("\n" + "=" * 45)
        print("             MARKS MANAGEMENT")
        print("=" * 45)

        print("1. Add Marks")
        print("2. View Marks")
        print("3. Update Marks")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_marks()

        elif choice == "2":
            view_marks()

        elif choice == "3":
            update_marks()

        elif choice == "4":
            break

        else:
            print("\n❌ Invalid choice. Please enter 1-4.")


def main():
    initialize_database()

    while True:
        print("\n" + "=" * 55)
        print("       STUDENT ACADEMIC PERFORMANCE SYSTEM")
        print("=" * 55)

        print("1. Student Management")
        print("2. Marks Management")
        print("3. Result Processing")
        print("4. Performance Analysis")
        print("5. Generate Report")
        print("6. Dashboard")
        print("7. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            student_management()

        elif choice == "2":
            marks_management()

        elif choice == "3":
            show_result()

        elif choice == "4":
            show_analysis()

        elif choice == "5":
            generate_report()

        elif choice == "6":
            show_dashboard()

        elif choice == "7":
            print("\nThank you for using the Student Academic Performance System!")
            print("Goodbye! 👋")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()