package com.resumechecker;

import java.util.ArrayList;
import java.util.List;

/**
 * ScoreCalculator
 * ----------------
 * Java version of the scoring logic found in resume_analyzer.py's
 * mock_analyze() function. Calculates a 0-100 resume score based on
 * how many known skills are found and how long the resume text is.
 */
public class ScoreCalculator {

    public static final String[] COMMON_SKILLS = {
        "python", "java", "javascript", "sql", "flask", "django", "react",
        "html", "css", "git", "github", "docker", "aws", "linux", "c++",
        "data structures", "algorithms", "machine learning", "communication",
        "teamwork", "leadership", "problem solving", "rest api", "testing"
    };

    /** Returns the list of common skills found inside the resume text. */
    public List<String> extractSkills(String text) {
        String lower = text.toLowerCase();
        List<String> found = new ArrayList<>();
        for (String skill : COMMON_SKILLS) {
            if (lower.contains(skill)) {
                found.add(skill);
            }
        }
        return found;
    }

    /** Calculates the resume score (capped at 100) using the same formula as Python. */
    public int calculateScore(String text) {
        List<String> foundSkills = extractSkills(text);
        int wordCount = text.trim().isEmpty() ? 0 : text.trim().split("\\s+").length;

        int score = 40 + (foundSkills.size() * 3) + Math.min(wordCount / 20, 20);
        return Math.min(score, 100);
    }

    /** Calculates the percentage of common skills matched. */
    public int calculateKeywordMatch(String text) {
        List<String> foundSkills = extractSkills(text);
        return (int) ((foundSkills.size() / (double) COMMON_SKILLS.length) * 100);
    }
}
