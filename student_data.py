"""
==================================================================
 student_data.py  --  SHARED CORE LOGIC
==================================================================
All file reading/writing and business logic lives here so that
BOTH interfaces to this project --
    1) main.py  (console menu app)
    2) app.py   (Flask web app)
-- use the exact same data and the exact same rules. Nothing here
prints anything; it just returns data or (success, message) tuples,
so either interface can present it however it wants.

Data storage format (students_data.txt):
    RollNumber,Name,Course,Mark
    101,Aarav Sharma,Computer Science,88.5
==================================================================
"""

import os
import csv

DATA_FILE = "students_data.txt"
EXPORT_FILE = "students_export.csv"


# ------------------------------------------------------------------
# FILE HANDLING
# ------------------------------------------------------------------

def initialize_file():
    """Create the data file with 5 default students if missing."""
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


def read_all_students():
    """Returns a list of dicts: {roll, name, course, mark}."""
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
                continue
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
    students = students if students is not None else read_all_students()
    return any(s["roll"] == roll for s in students)


# ------------------------------------------------------------------
# CORE OPERATIONS (return (success: bool, message: str))
# ------------------------------------------------------------------

def add_student(roll, name, course, mark):
    roll, name, course = roll.strip(), name.strip(), course.strip()

    if not roll or not name or not course:
        return False, "Roll Number, Name and Course cannot be empty."

    try:
        mark = float(mark)
    except (TypeError, ValueError):
        return False, "Mark must be a valid number."

    if not (0 <= mark <= 100):
        return False, "Mark must be between 0 and 100."

    if roll_exists(roll):
        return False, f"Roll Number {roll} already exists. Use a unique roll number."

    # Append mode -> never deletes existing records
    with open(DATA_FILE, "a") as f:
        f.write(f"{roll},{name},{course},{mark}\n")

    return True, f"Student '{name}' (Roll {roll}) added successfully."


def update_student(roll, name=None, course=None, mark=None):
    students = read_all_students()
    for s in students:
        if s["roll"] == roll:
            if name:
                s["name"] = name.strip()
            if course:
                s["course"] = course.strip()
            if mark:
                try:
                    mark_val = float(mark)
                    if 0 <= mark_val <= 100:
                        s["mark"] = mark_val
                    else:
                        return False, "Mark must be between 0 and 100."
                except ValueError:
                    return False, "Mark must be a valid number."
            write_all_students(students)
            return True, f"Roll {roll} updated successfully."
    return False, "Student not found."


def delete_student(roll):
    students = read_all_students()
    updated = [s for s in students if s["roll"] != roll]
    if len(updated) == len(students):
        return False, "Student not found."
    write_all_students(updated)
    return True, f"Roll {roll} deleted successfully."


def search_student(roll):
    """Returns the student dict, or None if not found."""
    for s in read_all_students():
        if s["roll"] == roll.strip():
            return s
    return None


def get_stats():
    """Returns dict: total, average (0 if no students)."""
    students = read_all_students()
    total = len(students)
    average = round(sum(s["mark"] for s in students) / total, 2) if total else 0
    return {"total": total, "average": average}


def find_topper():
    students = read_all_students()
    if not students:
        return None
    return max(students, key=lambda s: s["mark"])


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


def get_sorted_students(by="roll"):
    students = read_all_students()
    if by == "mark":
        students.sort(key=lambda s: s["mark"], reverse=True)
    elif by == "name":
        students.sort(key=lambda s: s["name"].lower())
    else:
        students.sort(key=lambda s: s["roll"])
    return students


def export_to_csv():
    students = read_all_students()
    with open(EXPORT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll Number", "Name", "Course", "Mark"])
        for s in students:
            writer.writerow([s["roll"], s["name"], s["course"], s["mark"]])
    return EXPORT_FILE