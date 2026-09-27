from database import get_connection
from result import calculate_result
from analysis import get_performance_data


def generate_report():
    """Generate a complete academic performance report."""

    print("\n" + "=" * 60)
    print("                 ACADEMIC REPORT")
    print("=" * 60)

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

    analysis = get_performance_data(registration_no)

    if analysis is None:
        print("\n❌ Performance data is not available.")
        return

    marks = analysis["marks"]

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

    print("\n")
    print("=" * 60)
    print("          STUDENT ACADEMIC PERFORMANCE REPORT")
    print("=" * 60)

    print(f"Name             : {result['name']}")
    print(f"Registration No. : {registration_no}")
    print(f"Semester         : {result['semester']}")
    print(f"Branch           : {result['branch']}")

    print("\n" + "-" * 60)
    print(f"{'Subject':<30}{'Marks':<15}{'Percentage'}")
    print("-" * 60)

    for subject in marks:
        percentage = (subject[1] / subject[2]) * 100

        print(
            f"{subject[0]:<30}"
            f"{subject[1]:<15.2f}"
            f"{percentage:.2f}%"
        )

    print("-" * 60)

    print(
        f"Total Marks      : "
        f"{result['total']:.2f}/{result['maximum']}"
    )

    print(
        f"Overall Percentage: "
        f"{result['percentage']:.2f}%"
    )

    print(f"Grade            : {result['grade']}")
    print(f"Result           : {result['result']}")

    print("\n" + "-" * 60)

    print(
        f"Highest Subject  : "
        f"{highest[0]} ({highest[1]:.2f}/{highest[2]})"
    )

    print(
        f"Lowest Subject   : "
        f"{lowest[0]} ({lowest[1]:.2f}/{lowest[2]})"
    )

    print(f"Performance      : {performance}")

    print("=" * 60)
    print("              END OF REPORT")
    print("=" * 60)