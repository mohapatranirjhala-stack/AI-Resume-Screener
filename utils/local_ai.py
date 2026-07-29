
def recruiter_fallback(
    resume_text,
    jd_text,
    score,
    grade,
    decision
):

    return {

        "recommendation":
        "Resume evaluated using ATS rule-based analysis.",


        "strengths":[
            "Resume contains relevant technical information.",
            "Candidate profile matches evaluated criteria.",
            "Resume structure has been analysed."
        ],


        "weaknesses":[
            "AI detailed reasoning unavailable temporarily.",
            "Improve measurable achievements.",
            "Add more role-specific keywords."
        ],


        "notes":
        "AI service temporarily unavailable. "
        "Local ATS engine results are displayed.",


        "recruiter_score": int(score),

        "grade": grade,

        "decision": decision

    }



def feedback_fallback():

    return {

        "feedback":
        "AI feedback temporarily unavailable. "
        "ATS engine analysis is available."

    }