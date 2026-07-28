
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def export_resume_pdf(resume_text, filename):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph("<b>ATS Optimized Resume</b>", styles["Title"])
    )

    story.append(
        Paragraph("<br/>", styles["Normal"])
    )

    for line in resume_text.split("\n"):

        story.append(
            Paragraph(line.replace(" ", "&nbsp;"), styles["BodyText"])
        )

    doc.build(story)