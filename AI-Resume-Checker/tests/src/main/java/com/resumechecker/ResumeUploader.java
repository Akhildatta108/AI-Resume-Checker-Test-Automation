package com.resumechecker;

import java.util.Set;

/**
 * ResumeUploader
 * ---------------
 * Java version of the upload validation logic in app.py's allowed_file()
 * function, plus a simple text report generator matching app.py's
 * /report route.
 */
public class ResumeUploader {

    private static final Set<String> ALLOWED_EXTENSIONS = Set.of("pdf", "docx");

    /** Returns true if the filename has an allowed extension (pdf or docx). */
    public boolean isAllowedFile(String filename) {
        if (filename == null || !filename.contains(".")) {
            return false;
        }
        String extension = filename.substring(filename.lastIndexOf('.') + 1).toLowerCase();
        return ALLOWED_EXTENSIONS.contains(extension);
    }

    /** Builds a simple plain-text report, similar to the Flask /report route. */
    public String generateReport(String filename, int score, int keywordMatch) {
        StringBuilder report = new StringBuilder();
        report.append("AI RESUME CHECKER - REPORT\n");
        report.append("===========================\n");
        report.append("File Name: ").append(filename).append("\n");
        report.append("OVERALL SCORE: ").append(score).append(" / 100\n");
        report.append("KEYWORD MATCH: ").append(keywordMatch).append("%\n");
        return report.toString();
    }
}
