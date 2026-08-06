"""
validator.py
-------------
Validates a resume's contact details and structure using simple
regular expressions and keyword checks. No external service needed.
"""

import re

REQUIRED_SECTIONS = ["education", "experience", "skills", "projects"]

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_PATTERN = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}"
LINKEDIN_PATTERN = r"(linkedin\.com/in/[A-Za-z0-9\-_/]+)"
GITHUB_PATTERN = r"(github\.com/[A-Za-z0-9\-_/]+)"


def validate_email(text):
    match = re.search(EMAIL_PATTERN, text)
    return match.group(0) if match else None


def validate_phone(text):
    match = re.search(PHONE_PATTERN, text)
    return match.group(0) if match else None


def validate_linkedin(text):
    match = re.search(LINKEDIN_PATTERN, text, re.IGNORECASE)
    return match.group(0) if match else None


def validate_github(text):
    match = re.search(GITHUB_PATTERN, text, re.IGNORECASE)
    return match.group(0) if match else None


def check_missing_sections(text):
    """Return the list of expected resume sections that are not present."""
    text_lower = text.lower()
    missing = [section for section in REQUIRED_SECTIONS if section not in text_lower]
    return missing


def check_duplicate_skills(skills_list):
    """Return skills that appear more than once (case-insensitive)."""
    seen = {}
    duplicates = []
    for skill in skills_list:
        key = skill.strip().lower()
        if not key:
            continue
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 2:  # only add once, the moment it becomes a duplicate
            duplicates.append(skill.strip())
    return duplicates


def validate_resume(text, skills_list=None):
    """
    Run every validation check and return one summary dictionary.
    'skills_list' is optional; if not provided, duplicate-skill check is skipped.
    """
    skills_list = skills_list or []

    return {
        "email": validate_email(text),
        "phone": validate_phone(text),
        "linkedin": validate_linkedin(text),
        "github": validate_github(text),
        "missing_sections": check_missing_sections(text),
        "duplicate_skills": check_duplicate_skills(skills_list),
    }
