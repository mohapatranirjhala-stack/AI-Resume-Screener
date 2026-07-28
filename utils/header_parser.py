
import re


def extract_header_details(text):

    details = {
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "leetcode": ""
    }

    email = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email:
        details["email"] = email.group()

    phone = re.search(
        r"(\+?\d[\d\s\-]{8,15})",
        text
    )

    if phone:
        details["phone"] = phone.group()

    linkedin = re.search(
        r"https?://(?:www\.)?linkedin\.com/[^\s]+",
        text
    )

    if linkedin:
        details["linkedin"] = linkedin.group()

    github = re.search(
        r"https?://(?:www\.)?github\.com/[^\s]+",
        text
    )

    if github:
        details["github"] = github.group()

    leetcode = re.search(
        r"https?://(?:www\.)?leetcode\.com/[^\s]+",
        text
    )

    if leetcode:
        details["leetcode"] = leetcode.group()

    return details