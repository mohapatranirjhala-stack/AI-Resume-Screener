
import re


def extract_resume_structure(resume_text):

    sections = {
        "summary": "",
        "email": "",
        "phone": "",
        "github": "",
        "linkedin": "",
        "skills": [],
        "projects": [],
        "experience": [],
        "education": [],
        "certifications": []
    }

    text = resume_text.replace("\r", "")

    # -------------------------
    # Contact Information
    # -------------------------

    email = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email:
        sections["email"] = email.group()

    phone = re.search(
        r"(\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    if phone:
        sections["phone"] = phone.group()

    github = re.search(
        r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_.-]+",
        text,
        re.IGNORECASE
    )

    if github:
        sections["github"] = github.group()

    linkedin = re.search(
        r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+",
        text,
        re.IGNORECASE
    )

    if linkedin:
        sections["linkedin"] = linkedin.group()

    # -------------------------
    # Section Detection
    # -------------------------

    patterns = {
        "skills": r"(?i)(technical skills|skills)",
        "projects": r"(?i)(projects|project experience)",
        "experience": r"(?i)(experience|work experience|internship)",
        "education": r"(?i)(education)",
        "certifications": r"(?i)(certifications|certificates)"
    }

    matches = []

    for key, pattern in patterns.items():

        match = re.search(pattern, text)

        if match:

            matches.append(
                (
                    match.start(),
                    key
                )
            )

    matches.sort()

    if matches:

        sections["summary"] = text[:matches[0][0]].strip()

        for i in range(len(matches)):

            start = matches[i][0]

            key = matches[i][1]

            end = len(text)

            if i != len(matches) - 1:
                end = matches[i + 1][0]

            content = text[start:end].strip()

            lines = [
                line.strip("-• ")
                for line in content.split("\n")
                if line.strip()
            ]

            # Remove section heading
            if len(lines) > 1:
                lines = lines[1:]

            sections[key] = lines

    else:

        sections["summary"] = text

    return sections