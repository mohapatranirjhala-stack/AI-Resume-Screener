

from utils.openrouter import client
from utils.json_parser import parse_llm_json


def generate_feedback(resume_text, jd_text, matched_skills, missing_skills):

    prompt = f"""
You are an expert Technical Recruiter.

Analyze the following resume against the given Job Description.

Resume:
{resume_text}

Job Description:
{jd_text}

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}

Generate:

1. Top 3 strengths
2. Top 3 weaknesses
3. Top 4 recommendations

Return ONLY valid JSON.

Do not use markdown.
Do not wrap the response inside ```json.
Do not add explanations.
Return exactly one JSON object.

Example:

{{
    "strengths":[
        "...",
        "...",
        "..."
    ],
    "weaknesses":[
        "...",
        "...",
        "..."
    ],
    "recommendations":[
        "...",
        "...",
        "...",
        "..."
    ]
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content

    try:
        return parse_llm_json(result)

    except Exception:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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

        result = response.choices[0].message.content

        return parse_llm_json(result)