
import re

from utils.skill_extractor import compare_skills
from utils.llm_scoring import llm_resume_score


# ----------------------------------------------------
# Skill Score
# ----------------------------------------------------

def calculate_skill_score(resume_text, jd_text):

    data = compare_skills(resume_text, jd_text)

    matched = len(data["matched"])
    total = max(len(data["jd_skills"]), 1)

    return round((matched / total) * 100, 2)


# ----------------------------------------------------
# Keyword Score
# ----------------------------------------------------

def calculate_keyword_score(resume_text, jd_text):

    words = set(
        re.findall(
            r"\b[a-zA-Z]+\b",
            jd_text.lower()
        )
    )

    resume = resume_text.lower()

    matched = 0

    for word in words:
        if word in resume:
            matched += 1

    return round(
        (matched / max(len(words), 1)) * 100,
        2
    )


# ----------------------------------------------------
# Section Score
# ----------------------------------------------------

def calculate_section_score(resume_text):

    resume = resume_text.lower()

    def check_section(keywords):

        for keyword in keywords:
            if keyword in resume:
                return 100

        return 0


    sections = {

        "Experience": check_section(
            [
                "work experience",
                "professional experience",
                "internship",
                "intern",
                "employment"
            ]
        ),

        "Projects": check_section(
            [
                "projects",
                "project"
            ]
        ),

        "Education": check_section(
            [
                "education",
                "b.tech",
                "bachelor",
                "university",
                "college"
            ]
        ),

        "Skills": check_section(
            [
                "skills",
                "technical skills",
                "technologies"
            ]
        ),

        "Summary": check_section(
            [
                "summary",
                "profile",
                "objective",
                "professional summary"
            ]
        )
    }


    overall = round(
        sum(sections.values()) / len(sections),
        2
    )


    return overall, sections



# ----------------------------------------------------
# Formatting Score
# ----------------------------------------------------

def calculate_format_score(resume_text):

    score = 100

    words = len(resume_text.split())

    if words < 250:
        score -= 20

    if words > 900:
        score -= 15

    if resume_text.count("\n") < 10:
        score -= 20


    return max(score, 0)



# ----------------------------------------------------
# Action Verb Score
# ----------------------------------------------------

def calculate_action_verb_score(resume_text):

    verbs = [

        "developed",
        "built",
        "implemented",
        "created",
        "designed",
        "optimized",
        "improved",
        "engineered",
        "deployed",
        "led",
        "managed",
        "achieved"

    ]


    resume = resume_text.lower()

    found = 0


    for verb in verbs:

        if verb in resume:
            found += 1


    return min(found * 10, 100)



# ----------------------------------------------------
# Quantification Score
# ----------------------------------------------------

def calculate_quantification_score(resume_text):

    numbers = re.findall(
        r"\d+",
        resume_text
    )

    return min(
        len(numbers) * 10,
        100
    )



# ----------------------------------------------------
# Experience Score
# ----------------------------------------------------

def calculate_experience_score(resume_text):

    resume = resume_text.lower()

    score = 0


    experience_keywords = [

        "intern",
        "internship",
        "software engineer",
        "developer",
        "engineer",
        "work experience",
        "professional experience"

    ]


    for word in experience_keywords:

        if word in resume:
            score += 20


    years = re.findall(
        r"20\d{2}",
        resume
    )

    score += min(
        len(years) * 10,
        30
    )


    verbs = [

        "developed",
        "implemented",
        "built",
        "created",
        "designed",
        "optimized"

    ]


    for verb in verbs:

        if verb in resume:
            score += 5


    return min(score, 100)



# ----------------------------------------------------
# Readability Score
# ----------------------------------------------------

def calculate_readability_score(resume_text):

    sentences = max(
        resume_text.count("."),
        1
    )

    words = len(
        resume_text.split()
    )


    avg = words / sentences


    if avg < 25:
        return 100

    if avg < 35:
        return 85

    if avg < 45:
        return 70


    return 55
    # ----------------------------------------------------
# Missing Keywords
# ----------------------------------------------------

def extract_missing_keywords(resume_text, jd_text):

    data = compare_skills(
        resume_text,
        jd_text
    )

    return data["missing"]



# ----------------------------------------------------
# Formatting Feedback
# ----------------------------------------------------

def formatting_feedback(resume_text):

    tips = []


    if len(resume_text.split()) < 250:

        tips.append(
            "Resume is too short. Add more technical details."
        )


    if "linkedin" not in resume_text.lower():

        tips.append(
            "Add LinkedIn profile."
        )


    if "github" not in resume_text.lower():

        tips.append(
            "Add GitHub profile."
        )


    if resume_text.count("\n") < 10:

        tips.append(
            "Improve spacing and section formatting."
        )


    return tips



# ----------------------------------------------------
# Final ATS
# ----------------------------------------------------

def calculate_advanced_ats(
    resume_text,
    jd_text,
    use_llm=True
):

    skill = calculate_skill_score(
        resume_text,
        jd_text
    )


    keyword = calculate_keyword_score(
        resume_text,
        jd_text
    )


    section, section_scores = calculate_section_score(
        resume_text
    )


    formatting = calculate_format_score(
        resume_text
    )


    action = calculate_action_verb_score(
        resume_text
    )


    impact = calculate_quantification_score(
        resume_text
    )


    experience = calculate_experience_score(
        resume_text
    )


    readability = calculate_readability_score(
        resume_text
    )


    # --------------------------------------------
    # LLM Score (Optional)
    # --------------------------------------------

    if use_llm:

        llm = llm_resume_score(
            resume_text,
            jd_text
        )

        llm_score = llm.get(
            "llm_score",
            0
        )

    else:

        llm_score = 0



    # --------------------------------------------
    # Final Score Calculation
    # --------------------------------------------

    final_score = round(

        skill * 0.30 +

        keyword * 0.20 +

        section * 0.10 +

        formatting * 0.10 +

        action * 0.10 +

        experience * 0.10 +

        impact * 0.10 +

        readability * 0.05 +

        (
            llm_score * 0.05
            if use_llm
            else 0
        ),

        2
    )


    return {

        "final_score": final_score,

        "skill_score": skill,

        "keyword_score": keyword,

        "section_score": section,

        "format_score": formatting,

        "action_score": action,

        "experience_score": experience,

        "impact_score": impact,

        "readability_score": readability,

        "llm_score": llm_score,

        "section_scores": section_scores,

        "missing_keywords": extract_missing_keywords(
            resume_text,
            jd_text
        ),

        "formatting_feedback": formatting_feedback(
            resume_text
        )

    }