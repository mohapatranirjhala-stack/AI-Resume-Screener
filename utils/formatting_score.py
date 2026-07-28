
import re


def formatting_score(resume_text):

    score = 100

    feedback = []

    if len(resume_text.split()) < 250:
        score -= 15
        feedback.append("Resume is too short.")

    if len(resume_text.split()) > 1000:
        score -= 10
        feedback.append("Resume is too lengthy.")

    if "@" not in resume_text:
        score -= 20
        feedback.append("Email missing.")

    if re.search(r"\d{10}", resume_text) is None:
        score -= 15
        feedback.append("Phone number missing.")

    if "github" not in resume_text.lower():
        score -= 10
        feedback.append("GitHub profile missing.")

    if "linkedin" not in resume_text.lower():
        score -= 10
        feedback.append("LinkedIn profile missing.")

    return {
        "score": max(score, 0),
        "feedback": feedback
    }