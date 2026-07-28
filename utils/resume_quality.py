
import re


def analyze_resume_quality(resume_text):

    text = resume_text.lower()

    action_verbs = [
        "developed",
        "built",
        "implemented",
        "created",
        "designed",
        "optimized",
        "improved",
        "managed",
        "led",
        "engineered",
        "deployed",
        "automated",
        "integrated",
        "tested",
        "analyzed",
        "delivered",
        "collaborated",
        "maintained",
        "resolved",
        "achieved",
        "increased",
        "reduced",
        "enhanced",
        "executed",
        "configured"
    ]

    certifications = [
        "aws",
        "azure",
        "gcp",
        "oracle",
        "coursera",
        "udemy",
        "nptel",
        "microsoft",
        "google",
        "certification"
    ]

    result = {
        "projects": False,
        "experience": False,
        "education": False,
        "certifications": False,
        "achievements": False,
        "github": False,
        "linkedin": False,
        "portfolio": False,
        "email": False,
        "phone": False,
        "summary": False,
        "skills": False,
        "word_count": 0,
        "bullet_points": 0,
        "section_count":0,
        "action_verbs": 0
    }

    result["projects"] = "project" in text

    result["experience"] = (
        "experience" in text
        or "internship" in text
        or "work experience" in text
    )

    result["education"] = "education" in text

    result["summary"] = (
        "summary" in text
        or "professional summary" in text
        or "profile" in text
    )

    result["skills"] = "skills" in text

    result["certifications"] = any(
        cert in text
        for cert in certifications
    )

    result["github"] = "github.com" in text

    result["linkedin"] = "linkedin.com" in text

    result["portfolio"] = (
        "portfolio" in text
        or "vercel.app" in text
        or ".dev" in text
        or ".me" in text
    )

    result["email"] = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text
        )
    )

    result["phone"] = bool(
        re.search(
            r"\+?\d[\d\s\-]{8,}",
            resume_text
        )
    )

    result["achievements"] = bool(
        re.search(
            r"\d+%|\d+\+|\$\d+|\d+\s*(users|downloads|projects|clients|employees)",
            text
        )
    )

    # ----------------------------------------
    # Resume Length
    # ----------------------------------------

    result["word_count"] = len(text.split())

    # ----------------------------------------
    # Bullet Points
    # ----------------------------------------

    result["bullet_points"] = (
        resume_text.count("•")
        + resume_text.count("-")
        + resume_text.count("*")
    )

    # ----------------------------------------
    # Resume Sections Count
    # ----------------------------------------

    section_count = 0

    for flag in [
        result["summary"],
        result["skills"],
        result["projects"],
        result["experience"],
        result["education"],
        result["certifications"]
    ]:

        if flag:
            section_count += 1

    result["section_count"] = section_count

    result["action_verbs"] = sum(
        text.count(word)
        for word in action_verbs
    )
    # ----------------------------------------
    # Detect Resume Sections
    # ----------------------------------------

    result["section_score"] = 0

    if result["skills"]:
        result["section_score"] += 25

    if result["projects"]:
        result["section_score"] += 25

    if result["experience"]:
        result["section_score"] += 25

    if result["education"]:
        result["section_score"] += 25

    return result