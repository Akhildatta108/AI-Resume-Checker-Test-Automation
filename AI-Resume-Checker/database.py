"""
database.py
------------
Handles all SQLite database operations for the AI Resume Checker.
Beginner note: SQLite stores everything in a single file (resume_checker.db)
so no separate database server is needed.
"""

import sqlite3
import os
from datetime import datetime

DB_NAME = "resume_checker.db"


def get_connection():
    """Create and return a new SQLite connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create the 'history' table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            score INTEGER NOT NULL,
            keyword_match INTEGER NOT NULL,
            missing_skills TEXT,
            strengths TEXT,
            weaknesses TEXT,
            suggestions TEXT,
            validation_summary TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(filename, analysis, validation):
    """
    Save one resume analysis + validation result into the database.
    Returns the new row's id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history
        (filename, score, keyword_match, missing_skills, strengths,
         weaknesses, suggestions, validation_summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        analysis["score"],
        analysis["keyword_match"],
        " | ".join(analysis["missing_keywords"]),
        " | ".join(analysis["strengths"]),
        " | ".join(analysis["weaknesses"]),
        " | ".join(analysis["suggestions"]),
        str(validation),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_history():
    """Return every past analysis, most recent first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_analysis_by_id(record_id):
    """Return a single analysis record by its id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row
