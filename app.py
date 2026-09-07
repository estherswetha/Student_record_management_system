"""
==================================================================
 STUDENT RECORD MANAGEMENT SYSTEM -- WEB VERSION (Flask)
==================================================================
Opens the same students_data.txt file used by the console app
(main.py) in a browser instead of a terminal. All the actual
read/write/search/stats logic lives in student_data.py, so the
console app and this web app are always perfectly in sync.

Run with:
    python app.py
Then open:
    http://127.0.0.1:5000
==================================================================
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_file

import student_data as db

app = Flask(__name__)
app.secret_key = "student-record-management-system"  # only used to sign flash messages

# Make db.get_grade usable directly inside the HTML template as a filter
app.jinja_env.filters["grade"] = db.get_grade


@app.route("/")
def index():
    tab = request.args.get("tab", "register")
    sort_by = request.args.get("sort", "roll")
    search_roll = request.args.get("search", "").strip()

    students = db.get_sorted_students(sort_by)
    stats = db.get_stats()
    topper = db.find_topper()

    search_result = db.search_student(search_roll) if search_roll else None
    searched = bool(search_roll)

    return render_template(
        "index.html",
        tab=tab,
        sort_by=sort_by,
        students=students,
        stats=stats,
        topper=topper,
        search_roll=search_roll,
        search_result=search_result,
        searched=searched,
    )


@app.route("/add", methods=["POST"])
def add():
    success, message = db.add_student(
        request.form.get("roll", ""),
        request.form.get("name", ""),
        request.form.get("course", ""),
        request.form.get("mark", ""),
    )
    flash(message, "success" if success else "error")
    return redirect(url_for("index", tab="add"))


@app.route("/update/<roll>", methods=["POST"])
def update(roll):
    success, message = db.update_student(
        roll,
        request.form.get("name") or None,
        request.form.get("course") or None,
        request.form.get("mark") or None,
    )
    flash(message, "success" if success else "error")
    return redirect(url_for("index", tab="register"))


@app.route("/delete/<roll>", methods=["POST"])
def delete(roll):
    success, message = db.delete_student(roll)
    flash(message, "success" if success else "error")
    return redirect(url_for("index", tab="register"))


@app.route("/export")
def export():
    filename = db.export_to_csv()
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    db.initialize_file()
    app.run(debug=True)