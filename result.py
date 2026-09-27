from database import get_connection


def calculate_result(registration_no):
    """Calculate total, percentage, grade and pass/fail result."""

    connection = get_connection()
    cursor = connection.cursor()

    # Get student details
    cursor.execute("""
        SELECT student_id, name, semester, branch
        FROM students
        WHERE registration_no = ?
    """, (registration_no,))

    student = cursor.fetchone()

    if not student:
        connection.close()
        return None

    student_id = student[0]

    # Get marks
    cursor.execute("""
        SELECT sub.subject_name, m.marks, sub.max_marks
        FROM marks m
        JOIN subjects sub
        ON m.subject_id = sub.subject_id
        WHERE m.student_id = ?
        ORDER BY sub.subject_id
    """, (student_id,))

    marks = cursor.fetchall()
    connection.close()

    if not marks:
        return None

    total_marks = sum(mark[1] for mark in marks)
    maximum_marks = sum(mark[2] for mark in marks)

    percentage = (total_marks / maximum_marks) * 100

    # Grade calculation
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B+"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    # Pass/Fail
    # A student must score at least 40 in every subject.
    passed = all(
        (mark[1] / mark[2]) * 100 >= 40
        for mark in marks
    )

    result = "PASS" if passed else "FAIL"

    return {
        "student_id": student[0],
        "name": student[1],
        "semester": student[2],
        "branch": student[3],
        "marks": marks,
        "total": total_marks,
        "maximum": maximum_marks,
        "percentage": percentage,
        "grade": grade,
        "result": result
    }


def show_result():
    """Display the complete result of a student."""

    print("\n" + "=" * 55)
    print("                 RESULT PROCESSING")
    print("=" * 55)

    registration_no = input(
        "Enter Registration Number: "
    ).strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    result = calculate_result(registration_no)

    if result is None:
        print("\n❌ Student not found or marks are not available.")
        return

    print("\n" + "=" * 55)
    print("                 STUDENT RESULT")
    print("=" * 55)

    print(f"Name             : {result['name']}")
    print(f"Registration No. : {registration_no}")
    print(f"Semester         : {result['semester']}")
    print(f"Branch           : {result['branch']}")

    print("\n" + "-" * 55)
    print(f"{'Subject':<30}{'Marks':<15}")
    print("-" * 55)

    for subject in result["marks"]:
        print(
            f"{subject[0]:<30}"
            f"{subject[1]:.2f}/{subject[2]}"
        )

    print("-" * 55)

    print(
        f"Total            : "
        f"{result['total']:.2f}/{result['maximum']}"
    )

    print(
        f"Percentage       : "
        f"{result['percentage']:.2f}%"
    )

    print(f"Grade            : {result['grade']}")
    print(f"Result           : {result['result']}")

    print("=" * 55)