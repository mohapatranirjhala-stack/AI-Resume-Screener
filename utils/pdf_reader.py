
import pdfplumber
import docx

def extract_text(uploaded_file):

    if uploaded_file.name.endswith(".pdf"):

        text = ""

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    elif uploaded_file.name.endswith(".docx"):

        document = docx.Document(uploaded_file)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    elif uploaded_file.name.endswith(".txt"):

        return uploaded_file.read().decode("utf-8")

    return ""