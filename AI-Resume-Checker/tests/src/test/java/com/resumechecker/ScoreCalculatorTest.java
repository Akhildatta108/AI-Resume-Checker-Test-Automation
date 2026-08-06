package com.resumechecker;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * ScoreCalculatorTest
 * ---------------------
 * Tests for the resume scoring logic (score out of 100 and keyword match %).
 */
class ScoreCalculatorTest {

    private ScoreCalculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new ScoreCalculator();
    }

    @Test
    @DisplayName("Score never exceeds 100")
    void testScoreDoesNotExceedMax() {
        // Build a very long resume packed with every known skill.
        StringBuilder text = new StringBuilder();
        for (String skill : ScoreCalculator.COMMON_SKILLS) {
            text.append(skill).append(" ");
        }
        for (int i = 0; i < 500; i++) {
            text.append("experience ");
        }
        int score = calculator.calculateScore(text.toString());
        assertTrue(score <= 100);
    }

    @Test
    @DisplayName("Empty resume text still returns the base score")
    void testEmptyTextGivesBaseScore() {
        int score = calculator.calculateScore("");
        assertEquals(40, score);
    }

    @Test
    @DisplayName("More matched skills increases the score")
    void testMoreSkillsIncreasesScore() {
        int scoreFewSkills = calculator.calculateScore("I know Python.");
        int scoreManySkills = calculator.calculateScore("I know Python, Java, SQL, Flask, React, Docker.");
        assertTrue(scoreManySkills > scoreFewSkills);
    }

    @Test
    @DisplayName("extractSkills finds only skills present in the text")
    void testExtractSkills() {
        List<String> skills = calculator.extractSkills("I use Python and SQL daily.");
        assertTrue(skills.contains("python"));
        assertTrue(skills.contains("sql"));
        assertFalse(skills.contains("java"));
    }

    @Test
    @DisplayName("Keyword match percentage is between 0 and 100")
    void testKeywordMatchRange() {
        int match = calculator.calculateKeywordMatch("Python Java SQL Flask");
        assertTrue(match >= 0 && match <= 100);
    }
}
