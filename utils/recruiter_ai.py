
from utils.gemini_client import client, MODEL
from utils.json_parser import parse_llm_json


def recruiter_analysis(resume_text, jd_text, score, grade, decision):

    prompt = f"""
You are a Senior Technical Recruiter.

Resume:
{resume_text}

Job Description:
{jd_text}

Professional ATS Score:
{score:.2f}

Official ATS Grade:
{grade}

Official Hiring Decision:
{decision}

Your task is ONLY to generate:

1. recommendation
2. exactly 3 strengths
3. exactly 3 weaknesses
4. recruiter notes
5. recruiter_score (0-100)

IMPORTANT:

- Do NOT change the grade.
- Do NOT change the hiring decision.
- recruiter_score must be between 0 and 100.
- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT use triple backticks.
- Return exactly one JSON object.

Return exactly this JSON:

{{
    "recommendation": "",
    "strengths": [
        "",
        "",
        ""
    ],
    "weaknesses": [
        "",
        "",
        ""
    ],
    "notes": "",
    "recruiter_score": 85
}}

Resume:

{resume_text}
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        recruiter = parse_llm_json(
            response.text
        )

    except Exception:

        recruiter = {

            "recommendation":
            "AI recruiter analysis is temporarily unavailable because the AI quota has been reached. Rule-based ATS analysis is being displayed.",

            "strengths": [
                "Resume successfully analysed using the ATS engine.",
                "Relevant technical skills were identified.",
                "Resume sections were evaluated successfully."
            ],

            "weaknesses": [
                "Detailed AI recruiter insights are temporarily unavailable.",
                "Include more quantified achievements where possible.",
                "Improve alignment with job-specific keywords."
            ],

            "notes":
            "Local recruiter analysis is currently being used. Fresh AI recommendations will automatically appear once the AI service becomes available again.",

            "recruiter_score": int(score)
        }

    # Always enforce our own grade & decision
    recruiter["grade"] = grade
    recruiter["decision"] = decision

    # Fallback if recruiter_score is missing
    if "recruiter_score" not in recruiter:
        recruiter["recruiter_score"] = int(score)

    return recruiter