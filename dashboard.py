from database import get_connection


def show_dashboard():
    """Display overall academic statistics."""

    connection = get_connection()
    cursor = connection.cursor()

    # Total number of students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total number of subjects
    cursor.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = cursor.fetchone()[0]

    # Number of students with marks entered
    cursor.execute("""
        SELECT DISTINCT student_id
        FROM marks
    """)
    students_with_marks = cursor.fetchall()

    passed_students = 0
    failed_students = 0
    percentages = []

    for student in students_with_marks:
        student_id = student[0]

        cursor.execute("""
            SELECT m.marks, s.max_marks
            FROM marks m
            JOIN subjects s
            ON m.subject_id = s.subject_id
            WHERE m.student_id = ?
        """, (student_id,))

        marks = cursor.fetchall()

        if not marks:
            continue

        total_marks = sum(mark[0] for mark in marks)
        maximum_marks = sum(mark[1] for mark in marks)

        percentage = (total_marks / maximum_marks) * 100
        percentages.append(percentage)

        passed = all(
            (mark[0] / mark[1]) * 100 >= 40
            for mark in marks
        )

        if passed:
            passed_students += 1
        else:
            failed_students += 1

    # Calculate overall average
    if percentages:
        average_percentage = sum(percentages) / len(percentages)
    else:
        average_percentage = 0

    connection.close()

    print("\n" + "=" * 50)
    print("        ACADEMIC PERFORMANCE DASHBOARD")
    print("=" * 50)

    print(f"\nTotal Students       : {total_students}")
    print(f"Total Subjects       : {total_subjects}")
    print(f"Students Passed      : {passed_students}")
    print(f"Students Failed      : {failed_students}")
    print(f"Average Percentage   : {average_percentage:.2f}%")

    print("\n" + "=" * 50)