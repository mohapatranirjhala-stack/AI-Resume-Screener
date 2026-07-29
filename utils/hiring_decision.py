
from utils.openrouter import client
from utils.json_parser import parse_llm_json


def generate_hiring_decision(
    ats_score,
    matched_skills,
    missing_skills,
    resume_text,
    jd_text
):

    prompt = f"""
You are a Senior Technical Recruiter.

Resume ATS Score:
{ats_score}

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}

Resume:
{resume_text}

Job Description:
{jd_text}

Evaluate the candidate.

Return ONLY JSON.

Example:
{{
    "ats_grade":"A",
    "recommendation":"Shortlist",
    "strengths":[
        "...",
        "...",
        "..."
    ],
    "weaknesses":[
        "...",
        "...",
        "..."
    ]
}}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "system",
                    "content": "Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return parse_llm_json(
            response.choices[0].message.content
        )

    except Exception:

        if ats_score >= 90:
            grade = "A+"
            recommendation = "Hire"

        elif ats_score >= 80:
            grade = "A"
            recommendation = "Hire"

        elif ats_score >= 70:
            grade = "B"
            recommendation = "Strong Consider"

        elif ats_score >= 60:
            grade = "C"
            recommendation = "Consider"

        else:
            grade = "D"
            recommendation = "Reject"

        return {

            "ats_grade": grade,

            "recommendation": recommendation,

            "strengths": [
                "Candidate evaluated using the ATS scoring engine.",
                "Relevant technical skills were identified.",
                "Resume matched against the provided job description."
            ],

            "weaknesses": [
                "Detailed AI hiring analysis is temporarily unavailable.",
                "Improve measurable achievements where possible.",
                "Increase role-specific keyword coverage."
            ]

        }