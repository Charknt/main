import csv
import os

# ---------------------- CONFIGURATION ----------------------

DEFAULT_FILE = "ano.csv"
DEFAULT_HEADER = [
    "student_id","last_name","first_name","section",
    "quiz1","quiz2","quiz3","quiz4","quiz5",
    "midterm","final","attendance_percent"
]


# ---------------------- CLEAN AND VALIDATE CSV ----------------------

def clean_ingest(filename=DEFAULT_FILE, header=DEFAULT_HEADER):
    """Reads a CSV file, validates each row, and separates valid and invalid data."""
    if not os.path.exists(filename):
        print("File not found.")
        return [], []

    valid_rows = []
    bad_rows = []

    # Read CSV file
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return [], []

    file_header = rows[0]
    data_rows = rows[1:]

    # Validate each row of the CSV file
    for row in data_rows:
        try:
            # Ensure row has complete columns
            while len(row) < len(file_header):
                row.append("")

            # Check for missing student ID
            if not row[0].strip():
                raise ValueError("Missing student_id")

            # Fill missing text columns
            for i in range(1, 4):
                if not row[i].strip():
                    row[i] = "none"

            # Validate numeric fields (quiz1–attendance)
            for i in range(4, 12):
                val = row[i].strip() if isinstance(row[i], str) else row[i]
                if val == "" or str(val).lower() == "none":
                    row[i] = None
                else:
                    try:
                        num_val = float(val)
                        if not (0 <= num_val <= 100):
                            raise ValueError(f"{header[i]} out of range")
                        row[i] = num_val
                    except ValueError:
                        row[i] = None

            valid_rows.append(row)

        except Exception as e:
            row.append(str(e))
            bad_rows.append(row)

    # Display summary of results
    print(f"\nValid rows: {len(valid_rows)}")
    print(f"Bad rows: {len(bad_rows)}")

    return valid_rows, bad_rows
