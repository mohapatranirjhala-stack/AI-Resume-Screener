
import re


def score_section(section_text, jd_keywords):

    if not section_text:
        return 0

    text = section_text.lower()

    matched = 0

    for keyword in jd_keywords:

        if keyword.lower() in text:
            matched += 1

    if len(jd_keywords) == 0:
        return 0

    score = (matched / len(jd_keywords)) * 100

    return round(score, 2)