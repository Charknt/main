import csv
import os
import statistics
import analytics              # Handles grade calculations and analytics
import array_operations        # Handles basic CSV operations (add, delete, sort, etc.)
from ingest import clean_ingest # Reads and validates CSV file
import reports                 # Creates summary reports
import at_risk                 # Exports list of at-risk students

# ----------------- CONFIGURATION ----------------------

FILENAME = "ano.csv"  # CSV file name

# Columns used in the student database
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

# Load and clean data from CSV file
valid_rows, _ = array_operations.clean_ingest("ano.csv", HEADER)



# ----------------- MAIN MENU ----------------------

def menu():
    """Main menu for the student CSV system"""
    while True:
        # Display options
        print("\n=== STUDENT CSV MENU ===")
        print("1. Add and Save Student(s)")
        print("2. Read CSV File")
        print("3. Delete Student by ID")
        print("4. Select Header column")
        print("5. Project Student Record by Student ID")
        print("6. Sort Student Data")
        print("7. Analytics and Reports")
        print("8. Exit")

        choice = input("Enter choice: ").strip()

 # ----------------- MENU CHOICES ----------------------

        if choice == "1":
            array_operations.add_data()  # Add new student record
        elif choice == "2":
            valid_rows, _ = array_operations.clean_ingest()  # Reload CSV
            if valid_rows:
                print("\n Valid rows:")
                for row in valid_rows:
                    print(row)
        elif choice == "3":
            array_operations.delete_data()  # Delete student by ID
        elif choice == "4":
            array_operations.select_column()  # Show selected column
        elif choice == "5":
            array_operations.select_row()  # Show record by ID
        elif choice == "6":
            array_operations.sort_data()  # Sort student data
        elif choice == "7":
            # Submenu for analytics and reports
            while True:
                print("\n=== ANALYTICS AND REPORTS MENU ===")
                print("a. Compute Weighted Grades")
                print("b. Grade Distribution (A–F)")
                print("c. Percentiles (Top/Bottom 10%)")
                print("d. Outlier Detection (±2 SD)")
                print("e. Improvement (Final vs Midterm)")
                print("f. Summary Report")
                print("g. At-Risk Students (Export CSV)")
                print("h. Back to Main Menu")

                sub = input("Select an option (a–h): ").lower().strip()

                # Call specific analytics/report functions
                if sub == "a":
                    analytics.compute_grades()
                elif sub == "b":
                    analytics.grade_distribution()
                elif sub == "c":
                    analytics.percentiles()
                elif sub == "d":
                    analytics.outliers()
                elif sub == "e":
                    analytics.improvement()
                elif sub == "f":
                    reports.summary_report()
                elif sub == "g":
                    at_risk.export_at_risk()  # Export students with low performance
                elif sub == "h":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "8": # Exit program
            print("Exiting program.")
            break

# ----------------- RUN PROGRAM ----------------------

menu()  # Start program by calling the menu function
