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

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    recruiter = parse_llm_json(
        response.text
    )

    # Always enforce our own grade & decision
    recruiter["grade"] = grade
    recruiter["decision"] = decision

    # Fallback if LLM doesn't return recruiter_score
    if "recruiter_score" not in recruiter:
        recruiter["recruiter_score"] = int(score)

    return recruiter