"""
app.py
-------
Main Flask application for the AI Resume Checker.
Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from werkzeug.utils import secure_filename

from database import init_db, save_analysis, get_history, get_analysis_by_id
from resume_parser import parse_resume
from resume_analyzer import analyze_resume
from validator import validate_resume

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"  # needed for flash messages

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Make sure the upload folder and database table exist before we start.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
init_db()


def allowed_file(filename):
    """Check the file extension is one we support."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Home page with the upload form."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Handle resume upload, parse it, analyze it, validate it, and save results."""
    if "resume" not in request.files:
        flash("No file part in the request.")
        return redirect(url_for("index"))

    file = request.files["resume"]

    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PDF and DOCX files are allowed.")
        return redirect(url_for("index"))

    # Save the file safely to the uploads folder.
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Step 1: Extract text from the resume.
    text = parse_resume(filepath)

    # Step 2: Run AI analysis (score, strengths, weaknesses, suggestions).
    analysis = analyze_resume(text)

    # Step 3: Validate contact info + structure.
    validation = validate_resume(text, analysis["found_skills"])

    # Step 4: Save everything to the SQLite database.
    record_id = save_analysis(filename, analysis, validation)

    return redirect(url_for("dashboard", record_id=record_id))


@app.route("/dashboard/<int:record_id>")
def dashboard(record_id):
    """Show the analysis results for one resume."""
    record = get_analysis_by_id(record_id)
    if record is None:
        flash("Analysis not found.")
        return redirect(url_for("index"))
    return render_template("dashboard.html", record=record)


@app.route("/history")
def history():
    """Show every past analysis, most recent first."""
    records = get_history()
    return render_template("history.html", records=records)


@app.route("/report/<int:record_id>")
def report(record_id):
    """Generate and download a plain-text report for one analysis."""
    record = get_analysis_by_id(record_id)
    if record is None:
        flash("Analysis not found.")
        return redirect(url_for("index"))

    report_text = f"""AI RESUME CHECKER - REPORT
===========================
File Name: {record['filename']}
Date: {record['created_at']}

OVERALL SCORE: {record['score']} / 100
KEYWORD MATCH: {record['keyword_match']}%

STRENGTHS:
- {record['strengths'].replace(' | ', chr(10) + '- ')}

WEAKNESSES:
- {record['weaknesses'].replace(' | ', chr(10) + '- ')}

MISSING KEYWORDS:
- {record['missing_skills'].replace(' | ', chr(10) + '- ')}

SUGGESTIONS:
- {record['suggestions'].replace(' | ', chr(10) + '- ')}

VALIDATION SUMMARY:
{record['validation_summary']}
"""
    return Response(
        report_text,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename=report_{record_id}.txt"},
    )


if __name__ == "__main__":
    app.run(debug=True)
