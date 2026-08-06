package com.resumechecker;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * ResumeValidator
 * ----------------
 * Java version of the validation rules found in validator.py.
 * Checks email, phone, LinkedIn, GitHub, and required sections.
 */
public class ResumeValidator {

    private static final String[] REQUIRED_SECTIONS = {
        "education", "experience", "skills", "projects"
    };

    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");

    private static final Pattern PHONE_PATTERN =
        Pattern.compile("(\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3,4}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{3,4}");

    private static final Pattern LINKEDIN_PATTERN =
        Pattern.compile("linkedin\\.com/in/[A-Za-z0-9\\-_/]+", Pattern.CASE_INSENSITIVE);

    private static final Pattern GITHUB_PATTERN =
        Pattern.compile("github\\.com/[A-Za-z0-9\\-_/]+", Pattern.CASE_INSENSITIVE);

    /** Returns the matched email, or null if none is found. */
    public String validateEmail(String text) {
        return findFirstMatch(EMAIL_PATTERN, text);
    }

    /** Returns the matched phone number, or null if none is found. */
    public String validatePhone(String text) {
        return findFirstMatch(PHONE_PATTERN, text);
    }

    /** Returns the matched LinkedIn URL, or null if none is found. */
    public String validateLinkedIn(String text) {
        return findFirstMatch(LINKEDIN_PATTERN, text);
    }

    /** Returns the matched GitHub URL, or null if none is found. */
    public String validateGitHub(String text) {
        return findFirstMatch(GITHUB_PATTERN, text);
    }

    /** Returns the list of required sections that are missing from the resume. */
    public List<String> checkMissingSections(String text) {
        String lower = text.toLowerCase();
        List<String> missing = new ArrayList<>();
        for (String section : REQUIRED_SECTIONS) {
            if (!lower.contains(section)) {
                missing.add(section);
            }
        }
        return missing;
    }

    /** Returns skills that appear more than once (case-insensitive). */
    public List<String> checkDuplicateSkills(List<String> skills) {
        List<String> duplicates = new ArrayList<>();
        List<String> seen = new ArrayList<>();
        for (String skill : skills) {
            String key = skill.trim().toLowerCase();
            if (key.isEmpty()) continue;
            if (seen.contains(key) && !duplicates.contains(skill.trim())) {
                duplicates.add(skill.trim());
            } else {
                seen.add(key);
            }
        }
        return duplicates;
    }

    private String findFirstMatch(Pattern pattern, String text) {
        Matcher matcher = pattern.matcher(text);
        return matcher.find() ? matcher.group() : null;
    }
}
