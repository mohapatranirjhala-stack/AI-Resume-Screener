
from utils.openrouter import client
from utils.json_parser import parse_llm_json


def generate_improvements(resume_text, jd_text):

    prompt = f"""
You are an ATS Resume Expert.

Analyze this resume against the job description.

Resume:
{resume_text}

Job Description:
{jd_text}

Suggest exactly 5 improvements.

Return ONLY JSON.

Example:

{{
    "improvements":[
        "...",
        "...",
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
            temperature=0.3
        )

        return parse_llm_json(
            response.choices[0].message.content
        )

    except Exception:

        return {

            "improvements": [

                "Include more measurable achievements using numbers and percentages.",

                "Add additional job-specific technical keywords that accurately reflect your experience.",

                "Strengthen project descriptions with action verbs and clear impact statements.",

                "Ensure every important ATS section (Summary, Skills, Projects, Experience and Education) is clearly structured.",

                "AI-generated improvement suggestions are temporarily unavailable. Rule-based ATS recommendations are currently being displayed."

            ]

        }