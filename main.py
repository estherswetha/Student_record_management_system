"""
==================================================================
 STUDENT RECORD MANAGEMENT SYSTEM
==================================================================
A file-based, menu-driven Python project that stores student
records (Roll Number, Name, Course, Mark) in a text file and lets
the user Add, View, Search, Update, Delete, and Analyze records.

Data storage format (students_data.txt):
    RollNumber,Name,Course,Mark
    101,Aarav Sharma,Computer Science,88.5

Author : (your name here)
==================================================================
"""

import os

DATA_FILE = "students_data.txt"


# ------------------------------------------------------------------
# UTILITY / FILE HANDLING FUNCTIONS
# ------------------------------------------------------------------

def initialize_file():
    """
    Create the data file with 5 default student records if the
    file does not already exist. This satisfies the requirement
    of 'store the details of 5 students' on first run.
    """
    if not os.path.exists(DATA_FILE):
        default_students = [
            "101,Aarav Sharma,Computer Science,88.5",
            "102,Priya Verma,Electronics,76.0",
            "103,Rohan Mehta,Mechanical,64.5",
            "104,Sneha Iyer,Computer Science,92.0",
            "105,Karthik Raj,Civil Engineering,58.0",
        ]
        with open(DATA_FILE, "w") as f:
            for line in default_students:
                f.write(line + "\n")
        print(f"[INFO] '{DATA_FILE}' not found. Created with 5 default records.\n")


def read_all_students():
    """
    Reads the data file and returns a list of dictionaries:
    [{"roll": "101", "name": "...", "course": "...", "mark": 88.5}, ...]
    Skips blank/corrupt lines instead of crashing the program.
    """
    students = []
    if not os.path.exists(DATA_FILE):
        return students

    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue  # skip malformed lines safely
            roll, name, course, mark = parts
            try:
                mark = float(mark)
            except ValueError:
                continue
            students.append(
                {"roll": roll.strip(), "name": name.strip(),
                 "course": course.strip(), "mark": mark}
            )
    return students


def write_all_students(students):
    """Rewrites the entire file from a list of student dicts."""
    with open(DATA_FILE, "w") as f:
        for s in students:
            f.write(f"{s['roll']},{s['name']},{s['course']},{s['mark']}\n")


def roll_exists(roll, students=None):
    """Check whether a roll number already exists in the file."""
    students = students if students is not None else read_all_students()
    return any(s["roll"] == roll for s in students)


def pause():
    input("\nPress Enter to return to the menu...")


# ------------------------------------------------------------------
# CORE FEATURES (as required in the problem statement)
# ------------------------------------------------------------------

def add_student():
    """
    Adds a new student record to the file WITHOUT deleting
    previous records (uses append mode 'a').
    """
    print("\n--- ADD NEW STUDENT ---")
    roll = input("Enter Roll Number: ").strip()

    if not roll:
        print("[ERROR] Roll Number cannot be empty.")
        return

    if roll_exists(roll):
        print(f"[ERROR] Roll Number {roll} already exists. Use a unique roll number.")
        return

    name = input("Enter Name: ").strip()
    course = input("Enter Course: ").strip()

    while True:
        mark_input = input("Enter Mark (0-100): ").strip()
        try:
            mark = float(mark_input)
            if 0 <= mark <= 100:
                break
            else:
                print("[ERROR] Mark must be between 0 and 100.")
        except ValueError:
            print("[ERROR] Please enter a valid number for mark.")

    if not name or not course:
        print("[ERROR] Name and Course cannot be empty.")
        return

    # Append mode -> does NOT delete existing records
    with open(DATA_FILE, "a") as f:
        f.write(f"{roll},{name},{course},{mark}\n")

    print(f"[SUCCESS] Student '{name}' (Roll {roll}) added successfully.")


def view_all_students():
    """Displays all student records in a neatly formatted table."""
    students = read_all_students()
    print("\n--- ALL STUDENT RECORDS ---")

    if not students:
        print("No records found.")
        return

    print(f"{'Roll No.':<10}{'Name':<20}{'Course':<20}{'Mark':<10}")
    print("-" * 60)
    for s in students:
        print(f"{s['roll']:<10}{s['name']:<20}{s['course']:<20}{s['mark']:<10}")
    print("-" * 60)
    print(f"Total Records: {len(students)}")


def search_student():
    """Asks for a Roll Number and displays the matching record, if any."""
    students = read_all_students()
    print("\n--- SEARCH STUDENT ---")
    roll = input("Enter Roll Number to search: ").strip()

    for s in students:
        if s["roll"] == roll:
            print("\n[FOUND] Student Details:")
            print(f"  Roll Number : {s['roll']}")
            print(f"  Name        : {s['name']}")
            print(f"  Course      : {s['course']}")
            print(f"  Mark        : {s['mark']}")
            return

    print("Student not found.")


def calculate_average():
    """Calculates and displays total number of students and average mark."""
    students = read_all_students()
    print("\n--- CLASS STATISTICS ---")

    if not students:
        print("No records found.")
        return

    total = len(students)
    avg = sum(s["mark"] for s in students) / total
    print(f"Total Students : {total}")
    print(f"Average Mark   : {avg:.2f}")


def find_topper():
    """Finds and displays the student with the highest mark."""
    students = read_all_students()
    print("\n--- TOPPER OF THE CLASS ---")

    if not students:
        print("No records found.")
        return

    topper = max(students, key=lambda s: s["mark"])
    print(f"  Roll Number : {topper['roll']}")
    print(f"  Name        : {topper['name']}")
    print(f"  Course      : {topper['course']}")
    print(f"  Mark        : {topper['mark']}")


# ------------------------------------------------------------------
# EXTRA / BONUS FEATURES (not required, but add real value)
# ------------------------------------------------------------------

def update_student():
    """EXTRA: Update an existing student's details."""
    students = read_all_students()
    print("\n--- UPDATE STUDENT ---")
    roll = input("Enter Roll Number to update: ").strip()

    for s in students:
        if s["roll"] == roll:
            print(f"Current details -> Name: {s['name']}, Course: {s['course']}, Mark: {s['mark']}")
            new_name = input("Enter new Name (leave blank to keep unchanged): ").strip()
            new_course = input("Enter new Course (leave blank to keep unchanged): ").strip()
            new_mark = input("Enter new Mark (leave blank to keep unchanged): ").strip()

            if new_name:
                s["name"] = new_name
            if new_course:
                s["course"] = new_course
            if new_mark:
                try:
                    s["mark"] = float(new_mark)
                except ValueError:
                    print("[WARNING] Invalid mark entered, mark left unchanged.")

            write_all_students(students)
            print("[SUCCESS] Student record updated.")
            return

    print("Student not found.")


def delete_student():
    """EXTRA: Delete a student record by Roll Number."""
    students = read_all_students()
    print("\n--- DELETE STUDENT ---")
    roll = input("Enter Roll Number to delete: ").strip()

    updated = [s for s in students if s["roll"] != roll]

    if len(updated) == len(students):
        print("Student not found.")
        return

    confirm = input(f"Are you sure you want to delete Roll {roll}? (y/n): ").strip().lower()
    if confirm == "y":
        write_all_students(updated)
        print("[SUCCESS] Student record deleted.")
    else:
        print("Deletion cancelled.")


def sort_students():
    """EXTRA: View students sorted by Mark (high to low) or Name (A-Z)."""
    students = read_all_students()
    if not students:
        print("\nNo records found.")
        return

    print("\n--- SORT STUDENTS ---")
    print("1. Sort by Mark (High to Low)")
    print("2. Sort by Name (A-Z)")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        students.sort(key=lambda s: s["mark"], reverse=True)
    elif choice == "2":
        students.sort(key=lambda s: s["name"].lower())
    else:
        print("Invalid option.")
        return

    print(f"\n{'Roll No.':<10}{'Name':<20}{'Course':<20}{'Mark':<10}")
    print("-" * 60)
    for s in students:
        print(f"{s['roll']:<10}{s['name']:<20}{s['course']:<20}{s['mark']:<10}")


def grade_report():
    """
    EXTRA: Assigns a letter grade to every student and shows a
    Pass/Fail summary (assuming 40 is the passing mark) plus a
    grade-wise distribution count.
    """
    students = read_all_students()
    if not students:
        print("\nNo records found.")
        return

    def get_grade(mark):
        if mark >= 90:
            return "A+"
        elif mark >= 80:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 60:
            return "C"
        elif mark >= 40:
            return "D"
        else:
            return "F"

    print("\n--- GRADE REPORT ---")
    print(f"{'Roll No.':<10}{'Name':<20}{'Mark':<10}{'Grade':<10}")
    print("-" * 50)

    grade_counts = {}
    pass_count = 0

    for s in students:
        grade = get_grade(s["mark"])
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
        if s["mark"] >= 40:
            pass_count += 1
        print(f"{s['roll']:<10}{s['name']:<20}{s['mark']:<10}{grade:<10}")

    print("-" * 50)
    print(f"Pass: {pass_count}  |  Fail: {len(students) - pass_count}")
    print("Grade distribution:", grade_counts)


def export_to_csv():
    """EXTRA: Export the records to a proper .csv file with headers."""
    import csv
    students = read_all_students()
    if not students:
        print("\nNo records found to export.")
        return

    filename = "students_export.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll Number", "Name", "Course", "Mark"])
        for s in students:
            writer.writerow([s["roll"], s["name"], s["course"], s["mark"]])

    print(f"[SUCCESS] Records exported to '{filename}'.")


# ------------------------------------------------------------------
# MENU-DRIVEN PROGRAM
# ------------------------------------------------------------------

def show_menu():
    print("\n" + "=" * 45)
    print("     STUDENT RECORD MANAGEMENT SYSTEM")
    print("=" * 45)
    print(" 1. Add Student")
    print(" 2. View All Students")
    print(" 3. Search Student")
    print(" 4. Find Average Mark")
    print(" 5. Find Topper")
    print(" 6. Update Student            (extra)")
    print(" 7. Delete Student            (extra)")
    print(" 8. Sort Students             (extra)")
    print(" 9. Grade Report (Pass/Fail)  (extra)")
    print("10. Export Records to CSV     (extra)")
    print(" 0. Exit")
    print("=" * 45)


def main():
    initialize_file()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            calculate_average()
        elif choice == "5":
            find_topper()
        elif choice == "6":
            update_student()
        elif choice == "7":
            delete_student()
        elif choice == "8":
            sort_students()
        elif choice == "9":
            grade_report()
        elif choice == "10":
            export_to_csv()
        elif choice == "0":
            print("\nExiting Student Record Management System. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please select a valid option from the menu.")

        pause()


if __name__ == "__main__":
    main()