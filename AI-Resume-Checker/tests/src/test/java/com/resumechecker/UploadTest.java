package com.resumechecker;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

/**
 * UploadTest
 * -----------
 * Tests for file-type validation on upload and report generation.
 */
class UploadTest {

    private ResumeUploader uploader;

    @BeforeEach
    void setUp() {
        uploader = new ResumeUploader();
    }

    @Test
    @DisplayName("Accepts a PDF file")
    void testAcceptsPdf() {
        assertTrue(uploader.isAllowedFile("my_resume.pdf"));
    }

    @Test
    @DisplayName("Accepts a DOCX file")
    void testAcceptsDocx() {
        assertTrue(uploader.isAllowedFile("my_resume.docx"));
    }

    @Test
    @DisplayName("Rejects unsupported file types")
    void testRejectsUnsupportedType() {
        assertFalse(uploader.isAllowedFile("my_resume.txt"));
        assertFalse(uploader.isAllowedFile("my_resume.exe"));
    }

    @Test
    @DisplayName("Rejects a filename with no extension")
    void testRejectsNoExtension() {
        assertFalse(uploader.isAllowedFile("my_resume"));
    }

    @Test
    @DisplayName("Rejects a null filename")
    void testRejectsNullFilename() {
        assertFalse(uploader.isAllowedFile(null));
    }

    @Test
    @DisplayName("Generated report contains key resume details")
    void testReportContainsDetails() {
        String report = uploader.generateReport("resume.pdf", 85, 70);
        assertTrue(report.contains("resume.pdf"));
        assertTrue(report.contains("85"));
        assertTrue(report.contains("70%"));
    }

    @Test
    @DisplayName("Generated report starts with the correct title")
    void testReportTitle() {
        String report = uploader.generateReport("resume.pdf", 90, 80);
        assertTrue(report.startsWith("AI RESUME CHECKER - REPORT"));
    }
}
