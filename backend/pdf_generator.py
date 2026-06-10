from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(report_text, filename):

    pdf = SimpleDocTemplate(
        f"reports/{filename}"
    )

    styles = getSampleStyleSheet()

    content = []

    for line in report_text.split("\n"):

        if line.strip():

            content.append(
                Paragraph(
                    line,
                    styles["Normal"]
                )
            )

    pdf.build(content)

    return filename