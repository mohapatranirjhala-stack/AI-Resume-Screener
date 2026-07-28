
from utils.pdf_reader import extract_text

def parse_job_description(uploaded_file):
    return extract_text(uploaded_file)