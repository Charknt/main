import csv
import os

# ---------------------- CONFIGURATION ----------------------

FILENAME = "ano.csv" # CSV file name
OUTPUT_FILE = "at_risk_students.csv"
PASSING_GRADE = 75.0  # Minimum passing threshold

# ---------------------- EXPORT AT-RISK STUDENTS ----------------------

def export_at_risk(filename=FILENAME, output_file=OUTPUT_FILE):
    """Identifies students below passing grade and exports to a new CSV file."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    if not reader:
        print("No data found.")
        return

    at_risk_students = []

    # Compute final grade for each student and flag those below passing grade
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

            quiz_avg = sum(quizzes) / len(quizzes)
            final_grade = (quiz_avg * 0.3) + (midterm * 0.3) + (final * 0.3) + (attendance * 0.1)

            if final_grade < PASSING_GRADE:
                at_risk_students.append({
                    "student_id": r.get("student_id", ""),
                    "last_name": r.get("last_name", ""),
                    "first_name": r.get("first_name", ""),
                    "section": r.get("section", ""),
                    "final_grade": f"{final_grade:.2f}",
                })

        except ValueError:
            continue

    # Display message if no at-risk students are found
    if not at_risk_students:
        print("No students are currently at risk.")
        return

    # Save at-risk students to a separate CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "last_name", "first_name", "section", "final_grade"])
        writer.writeheader()
        writer.writerows(at_risk_students)

    # Display formatted list of at-risk students
    print("\n=== AT-RISK STUDENTS ===")
    print("{:<12} {:<15} {:<15} {:<10} {:>10}".format("student_id", "last_name", "first_name", "section", "final_grade"))
    print("-" * 65)
    for s in at_risk_students:
        print(f"{s['student_id']:<12} {s['last_name']:<15} {s['first_name']:<15} {s['section']:<10} {s['final_grade']:>10}")

    print(f"\n{len(at_risk_students)} student(s) found below {PASSING_GRADE}.")
    print(f"Saved to: {output_file}")
