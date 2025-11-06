import csv
import os
import numpy as np  # For fast numerical operations

# ---------------- CONFIGURATION ----------------
FILENAME = "ano.csv"

# Grade weights (must total 1.0)
QUIZ_WEIGHT = 0.20
MIDTERM_WEIGHT = 0.30
FINAL_WEIGHT = 0.40
ATTENDANCE_WEIGHT = 0.10


# ---------------- WEIGHTED GRADE FUNCTION ----------------
def compute_weighted(row):
    """Calculate weighted grade for one student."""
    try:
        # Get quiz scores (skip blanks)
        quizzes = [
            float(row[f"quiz{i}"])
            for i in range(1, 6)
            if row[f"quiz{i}"] not in ("", "None", None)
        ]
        quizzes = np.array(quizzes, dtype=float)

        # Get other grades
        midterm = float(row["midterm"]) if row["midterm"] not in ("", "None", None) else np.nan
        final = float(row["final"]) if row["final"] not in ("", "None", None) else np.nan
        attendance = float(row.get("attendance_percent", 0)) if row.get("attendance_percent") not in ("", "None", None) else np.nan

        # Average quiz grade
        avg_quiz = np.nanmean(quizzes) if quizzes.size > 0 else np.nan

        # Combine grades and weights
        components = np.array([avg_quiz, midterm, final, attendance], dtype=float)
        weights = np.array([QUIZ_WEIGHT, MIDTERM_WEIGHT, FINAL_WEIGHT, ATTENDANCE_WEIGHT], dtype=float)

        # Handle missing data
        if np.isnan(components).all():
            return None
        components = np.nan_to_num(components, nan=0.0)

        # Weighted grade
        weighted = np.dot(components, weights)
        return round(float(weighted), 2)
    except Exception:
        return None


# ---------------- COMPUTE GRADES ----------------
def compute_grades(filename=FILENAME):
    """Show all students with their weighted grades."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        print("\n=== WEIGHTED GRADES ===")
        print("-" * 50)
        print(f"{'ID':<10}{'Name':<20}{'Weighted Grade':>15}")
        print("-" * 50)

        for row in reader:
            grade = compute_weighted(row)
            name = f"{row['last_name']}, {row['first_name']}"
            print(f"{row['student_id']:<10}{name:<20}{(grade if grade else 'N/A'):>15}")
        print("-" * 50)


# ---------------- GRADE DISTRIBUTION ----------------
def grade_distribution(filename=FILENAME):
    """Show grade counts (A–F)."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        grades = np.array([compute_weighted(r) for r in reader if compute_weighted(r)], dtype=float)

    bins = {
        "A": np.sum(grades >= 90),
        "B": np.sum((grades >= 80) & (grades < 90)),
        "C": np.sum((grades >= 70) & (grades < 80)),
        "D": np.sum((grades >= 60) & (grades < 70)),
        "F": np.sum(grades < 60),
    }

    print("\n=== GRADE DISTRIBUTION ===")
    for k, v in bins.items():
        print(f"{k}: {v}")


# ---------------- PERCENTILES ----------------
def percentiles(filename=FILENAME):
    """Show top and bottom 10% students."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    results = np.array(
        [(r["student_id"], compute_weighted(r)) for r in reader if compute_weighted(r)],
        dtype=object,
    )

    if results.size == 0:
        print("No valid grades.")
        return

    results = results[np.argsort(results[:, 1].astype(float))[::-1]]
    n = len(results)

    top = results[: max(1, n // 10)]
    bottom = results[-max(1, n // 10):]

    print("\n=== TOP 10% ===")
    for sid, g in top:
        print(f"{sid}: {float(g):.2f}")

    print("\n=== BOTTOM 10% ===")
    for sid, g in bottom:
        print(f"{sid}: {float(g):.2f}")


# ---------------- OUTLIERS ----------------
def outliers(filename=FILENAME):
    """Detect grades far from average (±1.5 SD)."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    grades, ids = [], []
    for r in reader:
        g = compute_weighted(r)
        if g:
            grades.append(float(g))
            ids.append(r["student_id"])

    if len(grades) < 2:
        print("Not enough data.")
        return

    grades = np.array(grades, dtype=float)
    mean, stdev = np.mean(grades), np.std(grades)

    print(f"\nMean = {mean:.2f}, SD = {stdev:.2f}")
    print("=== OUTLIERS ===")

    found = False
    for sid, g in zip(ids, grades):
        if abs(g - mean) > 1.5 * stdev:
            print(f"{sid}: {g:.2f}")
            found = True
    if not found:
        print("None found.")


# ---------------- IMPROVEMENT ----------------
def improvement(filename=FILENAME):
    """Compare midterm vs final grades."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    mids, finals, ids = [], [], []

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                mid = float(r["midterm"]) if r["midterm"] not in ("", "None", None) else np.nan
                fin = float(r["final"]) if r["final"] not in ("", "None", None) else np.nan
                mids.append(mid)
                finals.append(fin)
                ids.append(r["student_id"])
            except:
                continue

    mids, finals = np.array(mids, dtype=float), np.array(finals, dtype=float)
    diffs = finals - mids

    print("\n=== IMPROVEMENT (Final - Midterm) ===")
    for sid, diff in zip(ids, diffs):
        if not np.isnan(diff):
            sign = "+" if diff >= 0 else ""
            print(f"{sid}: {sign}{diff:.2f}")
