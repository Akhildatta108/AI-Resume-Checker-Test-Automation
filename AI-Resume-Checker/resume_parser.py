"""
resume_parser.py
-----------------
Extracts raw text from an uploaded resume file (.pdf or .docx).
"""

import os
from PyPDF2 import PdfReader
import docx


def extract_text_from_pdf(filepath):
    """Read every page of a PDF and return the combined text."""
    text = ""
    reader = PdfReader(filepath)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(filepath):
    """Read every paragraph of a Word document and return the combined text."""
    text = ""
    document = docx.Document(filepath)
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text


def parse_resume(filepath):
    """
    Detect the file type from its extension and extract text accordingly.
    Raises ValueError for unsupported file types.
    """
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(filepath)
    elif extension == ".docx":
        return extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
