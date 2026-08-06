"""
resume_analyzer.py
-------------------
Analyzes resume text and produces a score, strengths, weaknesses and
suggestions. If an OpenAI API key is configured, it uses the OpenAI API.
Otherwise it falls back to a simple rule-based "mock AI" so the project
still works out of the box with zero API cost.
"""

import os
import re

# A small skill dictionary used by the mock analyzer to match keywords.
# Feel free to extend this list for your own resume/job field.
COMMON_SKILLS = [
    "python", "java", "javascript", "sql", "flask", "django", "react",
    "html", "css", "git", "github", "docker", "aws", "linux", "c++",
    "data structures", "algorithms", "machine learning", "communication",
    "teamwork", "leadership", "problem solving", "rest api", "testing",
]


def extract_skills(text):
    """Find which common skills are mentioned in the resume text."""
    text_lower = text.lower()
    return [skill for skill in COMMON_SKILLS if skill in text_lower]


def mock_analyze(text):
    """
    Rule-based fallback analysis (used when no OpenAI API key is set).
    This keeps the project fully runnable without any paid API.
    """
    found_skills = extract_skills(text)
    missing_keywords = [s for s in COMMON_SKILLS if s not in found_skills][:5]

    word_count = len(text.split())
    keyword_match = int((len(found_skills) / len(COMMON_SKILLS)) * 100)

    # Very simple scoring formula: base score + bonus for skills/length.
    score = min(100, 40 + len(found_skills) * 3 + min(word_count // 20, 20))

    strengths = []
    weaknesses = []
    if len(found_skills) >= 5:
        strengths.append("Good range of technical skills mentioned")
    else:
        weaknesses.append("Few technical skills detected")

    if word_count >= 200:
        strengths.append("Resume has sufficient detail/length")
    else:
        weaknesses.append("Resume looks too short, add more detail")

    if "project" in text.lower():
        strengths.append("Includes project experience")
    else:
        weaknesses.append("No clear project section found")

    suggestions = [
        f"Consider adding these keywords: {', '.join(missing_keywords[:3])}",
        "Quantify achievements with numbers (e.g., 'improved speed by 30%')",
        "Keep bullet points concise and action-oriented",
    ]

    return {
        "score": score,
        "keyword_match": keyword_match,
        "found_skills": found_skills,
        "missing_keywords": missing_keywords,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }


def openai_analyze(text, api_key):
    """
    Real AI analysis using the OpenAI API.
    Only called when OPENAI_API_KEY is available.
    """
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    prompt = f"""
    Analyze the following resume text. Respond ONLY with plain text in
    exactly this format (no markdown):
    SCORE: <0-100 integer>
    KEYWORD_MATCH: <0-100 integer>
    STRENGTHS: <comma separated list>
    WEAKNESSES: <comma separated list>
    MISSING_KEYWORDS: <comma separated list>
    SUGGESTIONS: <comma separated list>

    Resume:
    {text[:3000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content

    # Parse the structured plain-text response into a dictionary.
    def grab(label):
        match = re.search(rf"{label}:\s*(.+)", content)
        return match.group(1).strip() if match else ""

    def to_list(value):
        return [v.strip() for v in value.split(",") if v.strip()]

    return {
        "score": int(re.sub(r"\D", "", grab("SCORE")) or 50),
        "keyword_match": int(re.sub(r"\D", "", grab("KEYWORD_MATCH")) or 50),
        "found_skills": extract_skills(text),
        "missing_keywords": to_list(grab("MISSING_KEYWORDS")),
        "strengths": to_list(grab("STRENGTHS")),
        "weaknesses": to_list(grab("WEAKNESSES")),
        "suggestions": to_list(grab("SUGGESTIONS")),
    }


def analyze_resume(text):
    """
    Main entry point. Uses OpenAI if OPENAI_API_KEY env var is set,
    otherwise automatically falls back to the mock analyzer.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            return openai_analyze(text, api_key)
        except Exception as error:
            print(f"OpenAI analysis failed, using mock analyzer instead: {error}")
            return mock_analyze(text)
    return mock_analyze(text)
