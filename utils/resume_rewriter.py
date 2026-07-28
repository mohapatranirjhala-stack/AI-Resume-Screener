
from utils.gemini_client import client, MODEL
from utils.json_parser import parse_llm_json


def rewrite_resume(original_resume):

    prompt = f"""
You are an expert ATS Resume Writer.

Rewrite the following resume professionally.

Rules:

- Keep ALL information truthful.
- Never invent experience.
- Never invent projects.
- Never invent certifications.
- Never invent skills.
- Improve grammar.
- Improve formatting.
- Improve readability.
- Use recruiter-friendly language.
- Use strong action verbs.
- Improve ATS compatibility.
- Preserve every section.
- Return the resume in plain text.
- Do NOT use Markdown.
- Do NOT use code blocks.

Return ONLY valid JSON.

{{
    "rewritten_resume":"Complete rewritten resume"
}}

Resume:

{original_resume}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    result = parse_llm_json(
        response.text
    )

    if not isinstance(result, dict):
        return {
            "rewritten_resume": original_resume
        }

    if "rewritten_resume" not in result:
        result["rewritten_resume"] = original_resume

    return result