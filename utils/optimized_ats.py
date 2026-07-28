
from utils.advanced_ats_engine import calculate_advanced_ats


def calculate_optimized_score(
    optimized_resume,
    jd_text
):

    ats = calculate_advanced_ats(
        optimized_resume,
        jd_text,
        use_llm=False
    )

    rule = ats["final_score"]

    llm_score = ats["llm_score"]

    final = ats["final_score"]

    return {

        "rule_score": rule,

        "llm_score": llm_score,

        "final_score": final,

        "skill_score": ats["skill_score"],

        "keyword_score": ats["keyword_score"],

        "section_score": ats["section_score"],

        "format_score": ats["format_score"],

        "action_score": ats["action_score"],

        "impact_score": ats["impact_score"],

        "readability_score": ats["readability_score"],

        "section_scores": ats["section_scores"],

        "missing_keywords": ats["missing_keywords"],

        "formatting_feedback": ats["formatting_feedback"]

    }