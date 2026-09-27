from database import get_connection


def get_performance_data(registration_no):
    """Get the student's marks for performance analysis."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, name
        FROM students
        WHERE registration_no = ?
    """, (registration_no,))

    student = cursor.fetchone()

    if not student:
        connection.close()
        return None

    cursor.execute("""
        SELECT sub.subject_name, m.marks, sub.max_marks
        FROM marks m
        JOIN subjects sub
        ON m.subject_id = sub.subject_id
        WHERE m.student_id = ?
        ORDER BY sub.subject_id
    """, (student[0],))

    marks = cursor.fetchall()
    connection.close()

    if not marks:
        return None

    return {
        "name": student[1],
        "marks": marks
    }


def show_analysis():
    """Display performance analysis for a student."""

    print("\n" + "=" * 55)
    print("             PERFORMANCE ANALYSIS")
    print("=" * 55)

    registration_no = input(
        "Enter Registration Number: "
    ).strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    data = get_performance_data(registration_no)

    if data is None:
        print("\n❌ Student not found or marks are not available.")
        return

    marks = data["marks"]

    percentages = [
        (subject[1] / subject[2]) * 100
        for subject in marks
    ]

    average = sum(percentages) / len(percentages)

    highest = max(
        marks,
        key=lambda subject: (subject[1] / subject[2]) * 100
    )

    lowest = min(
        marks,
        key=lambda subject: (subject[1] / subject[2]) * 100
    )

    if average >= 90:
        performance = "EXCELLENT"
    elif average >= 75:
        performance = "GOOD"
    elif average >= 60:
        performance = "AVERAGE"
    else:
        performance = "NEEDS IMPROVEMENT"

    print("\n" + "-" * 55)
    print(f"Student Name       : {data['name']}")
    print(f"Average Percentage  : {average:.2f}%")

    print(
        f"Highest Subject     : "
        f"{highest[0]} "
        f"({highest[1]:.2f}/{highest[2]})"
    )

    print(
        f"Lowest Subject      : "
        f"{lowest[0]} "
        f"({lowest[1]:.2f}/{lowest[2]})"
    )

    print(f"Performance Level   : {performance}")
    print("-" * 55)