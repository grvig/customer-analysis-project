from pdf_generator import create_pdf

sample_report = """
COMPLAINT ANALYSIS REPORT

Executive Summary

This is a test report.

Recommendations

Improve service quality.
"""

create_pdf(
    sample_report,
    "test_report.pdf"
)

print("PDF Created")