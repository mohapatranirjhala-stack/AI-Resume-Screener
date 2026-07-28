
from utils.skill_extractor import compare_skills
from utils.resume_quality import analyze_resume_quality
from utils.keyword_score import calculate_keyword_score


def calculate_ats_score(resume_text, jd_text):

    skills = compare_skills(resume_text, jd_text)
    quality = analyze_resume_quality(resume_text)

    from utils.skill_extractor import SKILL_PRIORITY

    matched_weight = 0
    total_weight = 0

    for skill in skills["jd_skills"]:

        weight = SKILL_PRIORITY.get(skill, 1)

        total_weight += weight

        if skill in skills["matched"]:
            matched_weight += weight

    if total_weight == 0:
        skill_score = 0
    else:
        skill_score = (matched_weight / total_weight) * 100

    # ----------------------------------------
    # Keyword Match Score (20%)
    # ----------------------------------------
    keyword_data = calculate_keyword_score(
        resume_text,
        jd_text
    )

    keyword_score = keyword_data["score"]

    # ----------------------------------------
    # Experience Score (15%)
    # ----------------------------------------

    experience_score = 0

    if quality["experience"]:
        experience_score += 50

    if quality["achievements"]:
        experience_score += 25

    if quality["action_verbs"] >= 10:
        experience_score += 25

    # ----------------------------------------
    # Project Score (10%)
    # ----------------------------------------

    project_score = 0

    if quality["projects"]:
        project_score += 60

    if quality["github"]:
        project_score += 20

    if quality["portfolio"]:
        project_score += 20

    # ----------------------------------------
    # Education Score (5%)
    # ----------------------------------------

    education_score = 100 if quality["education"] else 0

    # ----------------------------------------
    # ATS Formatting Score (10%)
    # ----------------------------------------

    formatting_score = 0

    if quality["email"]:
        formatting_score += 20

    if quality["phone"]:
        formatting_score += 20

    if quality["linkedin"]:
        formatting_score += 20

    if quality["projects"]:
        formatting_score += 20

    if quality["experience"]:
        formatting_score += 20

    # ----------------------------------------
    # Resume Quality Score (10%)
    # ----------------------------------------

    resume_quality_score = 0

    if quality["certifications"]:
        resume_quality_score += 30

    if quality["github"]:
        resume_quality_score += 20

    if quality["portfolio"]:
        resume_quality_score += 20

    if quality["action_verbs"] >= 10:
        resume_quality_score += 30

    resume_quality_score += quality["section_score"] * 0.20

    resume_quality_score = min(
        resume_quality_score,
        100
    )

    # ----------------------------------------
    # Final Professional ATS Score
    # ----------------------------------------

    final_score = (
        skill_score * 0.35 +
        keyword_score * 0.25 +
        experience_score * 0.15 +
        project_score * 0.10 +
        education_score * 0.05 +
        formatting_score * 0.05 +
        resume_quality_score * 0.05
    )

    # ----------------------------------------
    # Bonus ATS Factors
    # ----------------------------------------

    bonus = 0

    
    matched = len(skills["matched"])

    if matched >= 15:
        bonus += 5

    elif matched >= 10:
        bonus += 3

    elif matched >= 5:
        bonus += 1

    if quality["projects"] and quality["experience"]:
        bonus += 2

    if quality["github"] and quality["portfolio"]:
        bonus += 2

    if quality["action_verbs"] >= 15:
        bonus += 2

    final_score += bonus

    if final_score > 100:
        final_score = 100

    return {
        "skill_score": round(skill_score, 2),
        "keyword_score": round(keyword_score, 2),

        "experience_score": round(experience_score, 2),
        "project_score": round(project_score, 2),
        "education_score": round(education_score, 2),
        "formatting_score": round(formatting_score, 2),
        "resume_quality_score": round(resume_quality_score, 2),

        "matched_keywords": keyword_data["matched_keywords"],
        "missing_keywords": keyword_data["missing_keywords"],
        "matched_keyword_count": keyword_data["matched_count"],
        "missing_keyword_count": keyword_data["missing_count"],
        "total_keywords": keyword_data["total_keywords"],

        "resume_score": round(resume_quality_score, 2),

        "final_score": round(final_score, 2)
    }