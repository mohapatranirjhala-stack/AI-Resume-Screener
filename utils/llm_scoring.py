
from utils.openrouter import client
from utils.json_parser import parse_llm_json


def llm_resume_score(resume_text, jd_text):

    prompt = f"""
You are an Expert Technical Recruiter.

Evaluate this resume against the Job Description.

Resume:

{resume_text}

Job Description:

{jd_text}

Evaluate on:

1. Technical Skills (25)
2. Project Relevance (25)
3. Experience & Achievements (20)
4. ATS Formatting (15)
5. Communication & Resume Quality (15)

Return ONLY valid JSON.

{{
    "technical_score": 22,
    "project_score": 20,
    "experience_score": 16,
    "format_score": 13,
    "communication_score": 14,
    "llm_score": 85,
    "summary":"Excellent technical profile with relevant projects."
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "system",
                "content": """
                    Return ONLY valid JSON.

                    Do NOT use markdown.
                    Do NOT use triple backticks.
                    Do NOT include explanations.
                    Do NOT include comments.
                    Output must be valid JSON only.
                    """
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