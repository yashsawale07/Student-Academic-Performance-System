from database import get_connection


def add_student():
    """Add a new student to the database."""

    print("\n" + "=" * 45)
    print("             ADD STUDENT")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()
    name = input("Enter Student Name: ").strip()
    semester_input = input("Enter Semester: ").strip()
    branch = input("Enter Branch: ").strip()

    # Basic validation
    if not registration_no or not name or not semester_input or not branch:
        print("\n❌ All fields are required.")
        return

    if not semester_input.isdigit():
        print("\n❌ Semester must be a number.")
        return

    semester = int(semester_input)

    if semester < 1 or semester > 8:
        print("\n❌ Semester must be between 1 and 8.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (registration_no, name, semester, branch)
            VALUES (?, ?, ?, ?)
        """, (registration_no, name, semester, branch))

        connection.commit()

        print("\n✅ Student added successfully!")

    except Exception as error:
        if "UNIQUE constraint failed" in str(error):
            print("\n❌ Registration number already exists.")
        else:
            print("\n❌ Error:", error)

    finally:
        connection.close()


def search_student():
    """Search for a student using registration number."""

    print("\n" + "=" * 45)
    print("            SEARCH STUDENT")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, registration_no, name, semester, branch
        FROM students
        WHERE registration_no = ?
    """, (registration_no,))

    student = cursor.fetchone()
    connection.close()

    if student:
        print("\nStudent Found!")
        print("-" * 35)
        print(f"Student ID       : {student[0]}")
        print(f"Registration No. : {student[1]}")
        print(f"Name             : {student[2]}")
        print(f"Semester         : {student[3]}")
        print(f"Branch           : {student[4]}")
    else:
        print("\n❌ Student not found.")


def view_all_students():
    """Display all students."""

    print("\n" + "=" * 55)
    print("              ALL STUDENTS")
    print("=" * 55)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, registration_no, name, semester, branch
        FROM students
        ORDER BY student_id
    """)

    students = cursor.fetchall()
    connection.close()

    if not students:
        print("\nNo students found.")
        return

    print(
        f"{'ID':<5}"
        f"{'Registration No.':<20}"
        f"{'Name':<20}"
        f"{'Sem':<6}"
        f"{'Branch':<10}"
    )

    print("-" * 61)

    for student in students:
        print(
            f"{student[0]:<5}"
            f"{student[1]:<20}"
            f"{student[2]:<20}"
            f"{student[3]:<6}"
            f"{student[4]:<10}"
        )


def update_student():
    """Update an existing student's information."""

    print("\n" + "=" * 45)
    print("             UPDATE STUDENT")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, name, semester, branch
        FROM students
        WHERE registration_no = ?
    """, (registration_no,))

    student = cursor.fetchone()

    if not student:
        connection.close()
        print("\n❌ Student not found.")
        return

    print("\nLeave a field empty to keep its current value.")

    new_name = input(f"Name [{student[1]}]: ").strip()
    new_semester = input(f"Semester [{student[2]}]: ").strip()
    new_branch = input(f"Branch [{student[3]}]: ").strip()

    name = new_name if new_name else student[1]
    semester = student[2]
    branch = new_branch if new_branch else student[3]

    if new_semester:
        if not new_semester.isdigit():
            connection.close()
            print("\n❌ Semester must be a number.")
            return

        semester = int(new_semester)

        if semester < 1 or semester > 8:
            connection.close()
            print("\n❌ Semester must be between 1 and 8.")
            return

    cursor.execute("""
        UPDATE students
        SET name = ?, semester = ?, branch = ?
        WHERE registration_no = ?
    """, (name, semester, branch, registration_no))

    connection.commit()
    connection.close()

    print("\n✅ Student updated successfully!")


def delete_student():
    """Delete a student from the database."""

    print("\n" + "=" * 45)
    print("             DELETE STUDENT")
    print("=" * 45)

    registration_no = input("Enter Registration Number: ").strip()

    if not registration_no:
        print("\n❌ Registration number cannot be empty.")
        return

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
        print("\n❌ Student not found.")
        return

    print(f"\nStudent: {student[1]}")

    confirmation = input("Are you sure you want to delete this student? (y/n): ").strip().lower()

    if confirmation == "y":
        cursor.execute("""
            DELETE FROM marks
            WHERE student_id = ?
        """, (student[0],))

        cursor.execute("""
            DELETE FROM students
            WHERE student_id = ?
        """, (student[0],))

        connection.commit()

        print("\n✅ Student deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()