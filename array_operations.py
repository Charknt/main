import csv
import os
from ingest import clean_ingest  # Function to read and validate CSV data

# CSV file name and column headers
FILENAME = "ano.csv"
HEADER = [
    "student_id",
    "last_name",
    "first_name",
    "section",
    "quiz1",
    "quiz2",
    "quiz3",
    "quiz4",
    "quiz5",
    "midterm",
    "final",
    "attendance_percent"
]

# ---------------------- SAVE FUNCTIONS ----------------------

def save_to_csv(data, filename=FILENAME):
    """Appends new student data to CSV (adds header if file is new)."""
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerows(data)
    print(f"Data saved to {filename}")

def save_cleaned_csv(valid_rows, filename=FILENAME):
    """Overwrites CSV file with cleaned/updated data."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(valid_rows)
    print(f"Cleaned data saved to {filename}")

# ---------------------- ADD DATA ----------------------

def add_data():
    """Adds new student(s) with input validation."""
    new_rows = []
    n = int(input("How many students to add? "))

    for i in range(n):
        print(f"\n--- Student #{i+1} ---")
        print("--- student_id is required ---\n")
        student = []

        # Loop through each column in HEADER
        for idx, h in enumerate(HEADER):
            while True:
                val = input(f"Enter {h} (leave blank for 'none'): ").strip()

                # Validate student_id (must be unique)
                if idx == 0:
                    if not val:
                        print("Student_id cannot be empty. Try again.")
                        continue
                    
                    taken = False
                    with open("ano.csv") as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if val == row["student_id"]:
                                print("Student ID already taken, Try Again")
                                taken = True
                                break
                    if taken:
                        continue
                    student.append(val)
                    break

                # Validate names (no numbers)
                elif idx in [1, 2]:
                    if val == "":
                        val = "none"
                    elif any(char.isdigit() for char in val):
                        print("❌ Names cannot contain numbers. Try again.")
                        continue
                    student.append(val)
                    break

                # Section (letters or numbers allowed)
                elif idx == 3:
                    if val == "":
                        val = "none"
                    student.append(val)
                    break

                # Validate numeric fields (0–100)
                elif idx in range(4, 12):
                    if val == "" or val.lower() == "none":
                        student.append("none")
                        break
                    try:
                        num_val = float(val)
                        if not (0 <= num_val <= 100):
                            print("Score must be between 0 and 100. Try again.")
                            continue
                        student.append(num_val)
                        break
                    except ValueError:
                        print("Invalid number. Enter 0–100 or leave blank for 'none'.")
                        continue

        new_rows.append(student)

    save_to_csv(new_rows)  # Save all new students

# ---------------------- DELETE DATA ----------------------

def delete_data(filename=FILENAME):
    """Deletes a student by student_id."""
    if not os.path.exists(filename):
        print("File not found.")
        return

    student_id = input("Enter student_id to delete: ")
    valid_rows, _ = clean_ingest(filename, HEADER)
    updated_rows = [row for row in valid_rows if row[0] != student_id]

    if len(updated_rows) == len(valid_rows):
        print("No student found with that ID.")
        return

    save_cleaned_csv(updated_rows)
    print(f"Deleted student_id {student_id} successfully.")

# ---------------------- SELECT COLUMN ----------------------

def select_column(filename=FILENAME):
    """Displays all values under a selected column."""
    valid_rows, _ = clean_ingest(filename, HEADER)
    if not valid_rows:
        print("No valid data.")
        return

    print("\nAvailable columns:")
    for i, col in enumerate(HEADER):
        print(f"{i+1}. {col}")

    col_name = input("Enter column name to view: ").strip()
    if col_name not in HEADER:
        print("Invalid column name.")
        return

    index = HEADER.index(col_name)
    print(f"\nValues under '{col_name}':")
    for row in valid_rows:
        print(row[index])

# ---------------------- SELECT ROW ----------------------

def select_row(filename=FILENAME):
    """Displays full record of a student by student_id."""
    valid_rows, _ = clean_ingest(filename, HEADER)
    if not valid_rows:
        print("No valid data.")
        return

    student_id = input("Enter student_id to view: ")
    for row in valid_rows:
        if row[0] == student_id:
            print("\nStudent Information:")
            for h, v in zip(HEADER, row):
                print(f"{h}: {v}")
            return

    print("No student found with that ID.")

# ---------------------- SORT DATA ----------------------

def sort_data(filename=FILENAME):
    """Sorts data by a selected column."""
    valid_rows, _ = clean_ingest(filename, HEADER)
    if not valid_rows:
        print("No valid data to sort.")
        return

    print("\nAvailable columns to sort by:")
    for i, col in enumerate(HEADER):
        print(f"{i+1}. {col}")

    col_name = input("\nEnter column name to sort by: ").strip()
    if col_name not in HEADER:
        print("Invalid column name.")
        return

    col_index = HEADER.index(col_name)

    # Ask user for sorting order
    print("\nSort order:")
    print("1. Ascending (A→Z, 0→100)")
    print("2. Descending (Z→A, 100→0)")
    order = input("Enter choice (1 or 2): ").strip()
    reverse = True if order == "2" else False

    is_numeric = col_index in range(4, 12)  # Check if column is numeric

    # Define sorting key
    def sort_key(row):
        value = row[col_index]
        if is_numeric:
            if value is None:
                return float('-inf') if not reverse else float('inf')
            return float(value)
        else:
            if value is None or str(value).lower() == "none":
                return ""
            return str(value).lower()

    # Try to sort and show preview
    try:
        sorted_rows = sorted(valid_rows, key=sort_key, reverse=reverse)
        save_cleaned_csv(sorted_rows, filename)

        print(f"\nData sorted by '{col_name}' ({'descending' if reverse else 'ascending'})")
        print("\nPreview (first 10 rows):")
        print("-" * 100)
        print(f"{'ID':<12} {'Last Name':<15} {'First Name':<15} {'Section':<10} {col_name:<15}")
        print("-" * 100)
        for row in sorted_rows[:10]:
            display_val = row[col_index] if row[col_index] is not None else "N/A"
            print(f"{row[0]:<12} {row[1]:<15} {row[2]:<15} {row[3]:<10} {str(display_val):<15}")
        if len(sorted_rows) > 10:
            print(f"\n... and {len(sorted_rows) - 10} more rows")
    except Exception as e:
        print(f"Error during sorting: {e}")

# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    """Loads the CSV when the program starts."""
    valid, bad = clean_ingest(FILENAME, HEADER)
    print(f"Loaded {len(valid)} valid rows and {len(bad)} bad rows from {FILENAME}.")
