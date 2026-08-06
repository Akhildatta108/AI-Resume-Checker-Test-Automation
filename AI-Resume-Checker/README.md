# AI Resume Checker & Test Automation

An AI-powered web application that analyzes resumes (PDF/DOCX), scores them,
validates contact details and structure, and stores results in a history
dashboard — paired with a Java JUnit 5 test suite that verifies the core
logic. Built as a beginner-friendly, portfolio-ready Computer Science project.

---

## Project Overview

Upload a resume and the app will:
1. **Extract** the raw text from the PDF/DOCX file.
2. **Analyze** it with AI (OpenAI API, or an automatic mock analyzer if no
   API key is set) to produce a score, strengths, weaknesses, and suggestions.
3. **Validate** contact details (email, phone, LinkedIn, GitHub) and check
   for missing resume sections or duplicate skills.
4. **Save** the results to a local SQLite database.
5. **Display** everything on a dashboard, keep a full history, and let you
   **download a text report**.

A parallel **Java JUnit 5 test suite** re-implements the key validation and
scoring rules in Java and tests them — great practice for QA/test automation
skills alongside the Python/Flask web app.

---

## Features

| # | Feature | Description |
|---|---------|--------------|
| 1 | Resume Upload | Upload a PDF or DOCX resume through a simple drag-and-drop form |
| 2 | Resume Parsing | Extracts plain text from the uploaded file |
| 3 | AI Resume Analysis | Produces overall score, strengths, weaknesses, missing keywords, suggestions |
| 4 | Resume Validation | Checks email, phone, LinkedIn, GitHub, missing sections, duplicate skills |
| 5 | Dashboard | Shows score, keyword match %, missing skills, and suggestions visually |
| 6 | History | All past analyses are stored and browsable via SQLite |
| 7 | Reports | Download a plain-text report summarizing any analysis |
| 8 | Test Automation | Java JUnit 5 tests cover upload, validation, scoring, and reporting logic |

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **AI:** OpenAI API (falls back to a built-in rule-based mock analyzer if no API key is set)
- **Testing:** Java, JUnit 5, Maven

---

## Folder Structure

```
AI-Resume-Checker/
├── app.py                 # Flask app & routes
├── database.py             # SQLite setup + queries
├── resume_parser.py        # PDF/DOCX text extraction
├── resume_analyzer.py      # AI (or mock) resume analysis
├── validator.py            # Email/phone/section/duplicate validation
├── requirements.txt        # Python dependencies
├── .env.example             # Sample environment file for the OpenAI key
├── templates/
│   ├── index.html          # Upload page
│   ├── dashboard.html      # Analysis results page
│   └── history.html        # Past analyses list
├── static/
│   ├── css/style.css       # App styling
│   ├── js/script.js        # Drag-and-drop upload behavior
│   └── uploads/            # Uploaded resume files (created automatically)
├── tests/                  # Java JUnit 5 test suite (Maven project)
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/resumechecker/
│       │   ├── ResumeValidator.java
│       │   ├── ScoreCalculator.java
│       │   └── ResumeUploader.java
│       └── test/java/com/resumechecker/
│           ├── ResumeValidatorTest.java
│           ├── ScoreCalculatorTest.java
│           └── UploadTest.java
├── README.md
└── LICENSE
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/AI-Resume-Checker.git
cd AI-Resume-Checker
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Enable real AI analysis
Copy `.env.example` to `.env` and add your OpenAI API key:
```bash
cp .env.example .env
```
If you skip this step, the app automatically uses the built-in mock
analyzer, so it still works fully with **no API key required**.

### 5. Run the app
```bash
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

### 6. Run the Java tests (optional, requires Maven + JDK 17+)
```bash
cd tests
mvn test
```

---

## Screenshots

> Run the app locally and add your own screenshots here, for example:
> `![Upload Page](docs/screenshot-upload.png)`
>
> Suggested screenshots to capture:
> - Upload page with drag-and-drop area
> - Dashboard with score, strengths, weaknesses, and suggestions
> - History table of past analyses

---

## Future Improvements

- Support additional file types (e.g., `.txt`, `.rtf`)
- Add user accounts so history is scoped per user
- Compare resumes against a specific job description for tailored keyword matching
- Export reports as PDF instead of plain text
- Add CI pipeline (GitHub Actions) to run Java tests automatically on push
- Add Python unit tests (pytest) alongside the existing Java tests

---

## License

This project is licensed under the [MIT License](LICENSE).
