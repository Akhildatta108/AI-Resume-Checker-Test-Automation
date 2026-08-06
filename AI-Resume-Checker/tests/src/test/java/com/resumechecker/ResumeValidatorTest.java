package com.resumechecker;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * ResumeValidatorTest
 * --------------------
 * Tests for email/phone/LinkedIn/GitHub validation and missing
 * section / duplicate skill detection.
 */
class ResumeValidatorTest {

    private ResumeValidator validator;

    @BeforeEach
    void setUp() {
        validator = new ResumeValidator();
    }

    @Test
    @DisplayName("Detects a valid email address")
    void testValidEmailDetected() {
        String text = "Contact me at john.doe@example.com for more info.";
        assertEquals("john.doe@example.com", validator.validateEmail(text));
    }

    @Test
    @DisplayName("Returns null when no email is present")
    void testMissingEmail() {
        String text = "This resume has no contact email at all.";
        assertNull(validator.validateEmail(text));
    }

    @Test
    @DisplayName("Detects a valid phone number")
    void testValidPhoneDetected() {
        String text = "Phone: +1-555-123-4567";
        assertNotNull(validator.validatePhone(text));
    }

    @Test
    @DisplayName("Detects a LinkedIn profile URL")
    void testLinkedInDetected() {
        String text = "Profile: linkedin.com/in/johndoe";
        assertEquals("linkedin.com/in/johndoe", validator.validateLinkedIn(text));
    }

    @Test
    @DisplayName("Detects a GitHub profile URL")
    void testGitHubDetected() {
        String text = "GitHub: github.com/johndoe";
        assertEquals("github.com/johndoe", validator.validateGitHub(text));
    }

    @Test
    @DisplayName("Identifies missing resume sections")
    void testMissingSections() {
        String text = "Education: BSc Computer Science. Skills: Python, Java.";
        List<String> missing = validator.checkMissingSections(text);
        assertTrue(missing.contains("experience"));
        assertTrue(missing.contains("projects"));
        assertFalse(missing.contains("education"));
    }

    @Test
    @DisplayName("Returns no missing sections when all are present")
    void testNoMissingSections() {
        String text = "Education, Experience, Skills, and Projects are all here.";
        assertTrue(validator.checkMissingSections(text.toLowerCase()).isEmpty());
    }

    @Test
    @DisplayName("Detects duplicate skills in a list")
    void testDuplicateSkillsDetected() {
        List<String> skills = Arrays.asList("Python", "Java", "python", "SQL");
        List<String> duplicates = validator.checkDuplicateSkills(skills);
        assertEquals(1, duplicates.size());
    }

    @Test
    @DisplayName("Returns empty list when no skills are duplicated")
    void testNoDuplicateSkills() {
        List<String> skills = Arrays.asList("Python", "Java", "SQL");
        assertTrue(validator.checkDuplicateSkills(skills).isEmpty());
    }
}
