from database import get_connection


def find_student_id(registration_no):
    """Return student ID for a registration number."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id
        FROM students
        WHERE registration_no = ?
    """, (registration_no,))

    student = cursor.fetchone()
    connection.close()

    if student:
        return student[0]

    return None


def add_marks():
    """Add marks for a student."""

    print("\n" + "=" * 45)
    print("               ADD MARKS")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    student_id = find_student_id(registration_no)

    if student_id is None:
        print("\n❌ Student not found. Please add the student first.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject_id, subject_name, max_marks
        FROM subjects
        ORDER BY subject_id
    """)

    subjects = cursor.fetchall()

    print("\nEnter marks for each subject:")

    for subject in subjects:
        subject_id = subject[0]
        subject_name = subject[1]
        max_marks = subject[2]

        while True:
            marks_input = input(
                f"{subject_name} (0-{max_marks}): "
            ).strip()

            try:
                marks = float(marks_input)

                if marks < 0 or marks > max_marks:
                    print(
                        f"❌ Marks must be between 0 and {max_marks}."
                    )
                    continue

                break

            except ValueError:
                print("❌ Please enter a valid number.")

        cursor.execute("""
            SELECT mark_id
            FROM marks
            WHERE student_id = ? AND subject_id = ?
        """, (student_id, subject_id))

        existing_mark = cursor.fetchone()

        if existing_mark:
            cursor.execute("""
                UPDATE marks
                SET marks = ?
                WHERE student_id = ? AND subject_id = ?
            """, (marks, student_id, subject_id))
        else:
            cursor.execute("""
                INSERT INTO marks
                (student_id, subject_id, marks)
                VALUES (?, ?, ?)
            """, (student_id, subject_id, marks))

    connection.commit()
    connection.close()

    print("\n✅ Marks saved successfully!")


def view_marks():
    """Display marks of a student."""

    print("\n" + "=" * 45)
    print("               VIEW MARKS")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    student_id = find_student_id(registration_no)

    if student_id is None:
        print("\n❌ Student not found.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT s.name
        FROM students s
        WHERE s.student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

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

    print(f"\nStudent Name: {student[0]}")
    print(f"Registration No.: {registration_no}")

    print("\n" + "-" * 45)

    if not marks:
        print("No marks have been entered yet.")
        return

    print(f"{'Subject':<25}{'Marks':<10}{'Maximum'}")
    print("-" * 45)

    for mark in marks:
        print(
            f"{mark[0]:<25}"
            f"{mark[1]:<10.2f}"
            f"{mark[2]}"
        )


def update_marks():
    """Update marks for one subject."""

    print("\n" + "=" * 45)
    print("              UPDATE MARKS")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    student_id = find_student_id(registration_no)

    if student_id is None:
        print("\n❌ Student not found.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT sub.subject_id, sub.subject_name, m.marks, sub.max_marks
        FROM marks m
        JOIN subjects sub
        ON m.subject_id = sub.subject_id
        WHERE m.student_id = ?
        ORDER BY sub.subject_id
    """, (student_id,))

    existing_marks = cursor.fetchall()

    if not existing_marks:
        connection.close()
        print("\n❌ No marks found for this student.")
        return

    print("\nCurrent Marks:")

    for index, mark in enumerate(existing_marks, start=1):
        print(
            f"{index}. {mark[1]} → "
            f"{mark[2]}/{mark[3]}"
        )

    choice = input(
        "\nEnter the number of the subject to update: "
    ).strip()

    if not choice.isdigit():
        connection.close()
        print("\n❌ Please enter a valid number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(existing_marks):
        connection.close()
        print("\n❌ Invalid subject selection.")
        return

    selected = existing_marks[choice - 1]

    while True:
        new_marks_input = input(
            f"Enter new marks for {selected[1]} "
            f"(0-{selected[3]}): "
        ).strip()

        try:
            new_marks = float(new_marks_input)

            if new_marks < 0 or new_marks > selected[3]:
                print(
                    f"❌ Marks must be between 0 and {selected[3]}."
                )
                continue

            break

        except ValueError:
            print("❌ Please enter a valid number.")

    cursor.execute("""
        UPDATE marks
        SET marks = ?
        WHERE student_id = ? AND subject_id = ?
    """, (new_marks, student_id, selected[0]))

    connection.commit()
    connection.close()

    print("\n✅ Marks updated successfully!")