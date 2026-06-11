import re
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import (
    TA_CENTER,
    TA_JUSTIFY
)

def clean_report_text(text):

    text = text.replace("**", "")
    text = text.replace("##", "")
    text = text.replace("# ", "")
    text = text.replace("---", "")

    text = re.sub(
        r'(\w+)\s*\n\s*\1(\w+)',
        r'\1\2',
        text
    )

    text = re.sub(
        r'\b(\w+)\s*\n\s*\1\b',
        r'\1',
        text
    )

    text = re.sub(
        r'Prepared by:.*',
        '',
        text,
        flags=re.DOTALL
    )

    return text.strip()

def add_page_number(canvas, doc):

    page_num = canvas.getPageNumber()

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9
    )

    canvas.drawString(
        50,
        30,
        "MYTVS Customer Analysis Dashboard"
    )

    canvas.drawRightString(
        550,
        30,
        f"Page {page_num}"
    )

    canvas.restoreState()

def create_pdf(report_text, filename):

    report_text = clean_report_text(
        report_text
    )

    pdf = SimpleDocTemplate(
        f"reports/{filename}",
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    metadata_style = ParagraphStyle(
        "Metadata",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        spaceBefore=16,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    list_style = ParagraphStyle(
        "List",
        parent=body_style,
        leftIndent=20,
        spaceBefore=2,
        spaceAfter=4
    )

    content = []

    headings = [
        "Executive Summary",
        "Top Complaint Categories",
        "Branch Analysis",
        "High Priority Issues",
        "Customer Satisfaction",
        "Recommendations",
        "Top Revenue Services",
        "Branch Revenue Analysis",
        "Average Service Cost",
        "Top Rated Branches",
        "Revenue Performance",
        "Complaint Analysis",
        "Overall Branch Assessment",
        "Average Customer Rating",
        "Return Intent Analysis",
        "Recommendation Analysis",
        "Feedback Insights"
    ]

    lines = report_text.split("\n")

    first_heading_done = False

    report_title = ""
    report_type = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if not first_heading_done:

            report_title = line

            report_type = (
                line.title()
                .replace("Report", "")
                .strip()
            )

            content.append(
                Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                body_style
                )
            )

            generated_date = datetime.now().strftime(
                "%d-%b-%Y %H:%M"
            )

            content.append(
                Paragraph(
                    f"""
                    Generated On: {generated_date}<br/>
                    Report Type: {report_type}
                    """,
                    metadata_style
                )
            )

            content.append(
                Spacer(1, 10)
            )

            first_heading_done = True

            continue

        if line in headings:

            content.append(
                Paragraph(
                    line,
                    heading_style
                )
            )

            continue

        if re.match(r'^\d+\.', line):

            content.append(
                Paragraph(
                    line,
                    list_style
                )
            )

            continue

        if line.startswith("-"):

            content.append(
                Paragraph(
                    line,
                    list_style
                )
            )

            continue

        content.append(
            Paragraph(
                line,
                body_style
            )
        )

    pdf.build(
        content,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return filename