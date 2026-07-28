
from utils.openrouter import client
from utils.json_parser import parse_llm_json


def validate_resume(original_resume, optimized_resume):

    prompt = f"""
You are an Expert Resume Auditor.

Compare these two resumes.

ORIGINAL RESUME

{original_resume}

OPTIMIZED RESUME

{optimized_resume}

Check whether the optimized resume introduced fake information.

Verify:

1. Skills
2. Projects
3. Experience
4. Education
5. Certifications
6. Technologies

Return ONLY JSON.

{{
    "overall_verdict":"Safe",
    "hallucination_detected":"No",
    "truthfulness_score":100,
    "verified_sections":[
        "",
        "",
        ""
    ],
    "warnings":[
        ""
    ],
    "summary":""
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
        temperature=0
    )

    return parse_llm_json(
        response.choices[0].message.content
    )