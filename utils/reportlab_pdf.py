
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics


def generate_reportlab_pdf(resume_text, output_file):

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    body_style = styles["BodyText"]

    pdf = SimpleDocTemplate(output_file)

    elements = []

    elements.append(
        Paragraph("ATS Optimized Resume", title_style)
    )

    elements.append(
        Paragraph("<br/>", body_style)
    )

    lines = resume_text.split("\n")

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        if line.isupper():

            elements.append(
                Paragraph(line, heading_style)
            )

        else:

            line = line.replace("&", "&amp;")
            line = line.replace("<", "&lt;")
            line = line.replace(">", "&gt;")

            elements.append(
                Paragraph(line, body_style)
            )

    pdf.build(elements)

    return output_file