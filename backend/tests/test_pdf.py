import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from pdf_generator import create_pdf

SAMPLE_REPORT = """
## SUMMARY

This is a test report for PDF generation.

## RECOMMENDATIONS

- Improve service quality.
- Follow up with customers.
"""

def test_pdf_creates_file():
    filename = "test_output.pdf"
    create_pdf(SAMPLE_REPORT, filename)
    filepath = os.path.join("reports", filename)
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0
    os.remove(filepath)
