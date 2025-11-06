import csv
import os
import statistics

# ---------------------- CONFIGURATION ----------------------

FILENAME = "ano.csv"  # CSV file name


# ---------------------- Generate Summary Report ----------------------

def summary_report(filename=FILENAME):
    """Compute and print a summary of all student final grades."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    # Read the CSV file
    with open(filename, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    if not reader:
        print("No data in CSV.")
        return

    # Display the table header
    print("\n=== SUMMARY REPORT ===")
    print("{:<12} {:<15} {:<15} {:<10} {:>10}".format(
        "student_id", "last_name", "first_name", "section", "final_grade"
    ))
    print("-" * 65)

    grades = []

    # Compute weighted grades for each student
    for r in reader:
        try:
            quizzes = [
                float(r.get("quiz1", 0) or 0),
                float(r.get("quiz2", 0) or 0),
                float(r.get("quiz3", 0) or 0),
                float(r.get("quiz4", 0) or 0),
                float(r.get("quiz5", 0) or 0),
            ]
            midterm = float(r.get("midterm", 0) or 0)
            final = float(r.get("final", 0) or 0)
            attendance = float(r.get("attendance_percent", 0) or 0)

            # Weighted formula for computing the final grade
            quiz_avg = sum(quizzes) / len(quizzes)
            final_grade = (quiz_avg * 0.3) + (midterm * 0.3) + (final * 0.3) + (attendance * 0.1)

            grades.append(final_grade)

            # Print each student's details
            print("{:<12} {:<15} {:<15} {:<10} {:>10.2f}".format(
                r.get("student_id", ""),
                r.get("last_name", ""),
                r.get("first_name", ""),
                r.get("section", ""),
                final_grade
            ))

        except ValueError:
            continue

    # Display overall statistics
    if not grades:
        print("\nNo valid grade data available.")
        return

    print("\n--- SUMMARY STATISTICS ---")
    print(f"Total Students: {len(grades)}")
    print(f"Average Grade: {statistics.mean(grades):.2f}")
    print(f"Highest Grade: {max(grades):.2f}")
    print(f"Lowest Grade:  {min(grades):.2f}")
