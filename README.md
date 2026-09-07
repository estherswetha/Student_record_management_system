Student Record Management System (Python)

A simple, file-based, menu-driven console project. No external libraries or database needed — just Python's built-in file handling.

📁 Folder structure (exactly what you should have in VS Code)
student_record_management_system/     <-- open THIS folder in VS Code
├── main.py                 # the entire program (run this file)
├── students_data.txt       # data storage (auto-created if missing)
└── README.md                # this file

After you run the "Export to CSV" menu option once, you'll also see:

└── students_export.csv     # generated automatically, ignore/delete anytime
▶️ How to run in VS Code
Install Python from python.org if you don't have it (VS Code will also prompt you to install the "Python" extension by Microsoft — accept that).
Open VS Code → File > Open Folder... → select the student_record_management_system folder.
Open main.py.
Run it either by:
Clicking the ▶ Run button (top-right), or
Opening a terminal (Ctrl+`) and typing:
     python main.py
 (On Mac/Linux you may need `python3 main.py`)

5. The menu will appear in the terminal. Type a number and press Enter.

That's it — no pip install required, since the project only uses Python's standard library (os, csv).

📋 Data format

Each line in students_data.txt is one student, comma-separated:

RollNumber,Name,Course,Mark
101,Aarav Sharma,Computer Science,88.5

The file is created automatically with 5 sample students the first time you run main.py, so you don't need to create it by hand.

✅ Core features (as required)
#	Feature	Menu option
1	Store 5 initial student records in a file	(auto on first run)
2	Add new students without deleting old ones (append mode)	1
3	Display all student records	2
4	Search a student by Roll Number ("Student not found" if missing)	3
5	Total number of students + average mark	4
6	Find and display the topper (highest mark)	5
7	Menu-driven interface for everything above	(the main menu)
✨ Extra features added on top
Menu option	Feature	Why it's useful
6	Update Student	Fix a typo or update marks without deleting & re-adding
7	Delete Student	Remove a record permanently (with a confirmation prompt)
8	Sort Students	View the list sorted by Mark (high→low) or Name (A→Z)
9	Grade Report	Auto-assigns A+/A/B/C/D/F grades + Pass/Fail count + grade distribution
10	Export to CSV	Creates students_export.csv — opens directly in Excel/Google Sheets

Plus, under the hood:

Input validation: marks must be numeric and between 0–100; empty names/roll numbers are rejected.
Duplicate roll number protection: won't let you add two students with the same Roll Number.
Corrupt-line protection: if a line in the text file is damaged, it's skipped instead of crashing the whole program.
Clean tabular console output for easy reading.
🧪 Example run
=============================================
     STUDENT RECORD MANAGEMENT SYSTEM
=============================================
 1. Add Student
 2. View All Students
 3. Search Student
 4. Find Average Mark
 5. Find Topper
 6. Update Student            (extra)
 7. Delete Student            (extra)
 8. Sort Students             (extra)
 9. Grade Report (Pass/Fail)  (extra)
10. Export Records to CSV     (extra)
 0. Exit
=============================================
Enter your choice: 2

--- ALL STUDENT RECORDS ---
Roll No.  Name                Course              Mark
------------------------------------------------------------
101       Aarav Sharma        Computer Science    88.5
102       Priya Verma         Electronics         76.0
103       Rohan Mehta         Mechanical          64.5
104       Sneha Iyer          Computer Science    92.0
105       Karthik Raj         Civil Engineering   58.0
------------------------------------------------------------
Total Records: 5
