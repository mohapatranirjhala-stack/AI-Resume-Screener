
from utils.openrouter import client
from utils.json_parser import parse_llm_json


def optimize_resume(resume_text, jd_text):

    prompt = f"""
You are an Expert ATS Resume Writer, Resume Reviewer and Senior Technical Recruiter.

Your objective is to rewrite the resume so that it performs significantly better in Applicant Tracking Systems (ATS) while remaining completely truthful.

========================
Candidate Resume
========================

{resume_text}

========================
Job Description
========================

{jd_text}

STRICT RULES

1. NEVER invent any new skill.
2. NEVER invent any internship.
3. NEVER invent any certification.
4. NEVER invent any company.
5. NEVER invent any project.
6. NEVER invent any technology.
7. NEVER invent achievements.
8. NEVER change education.
9. NEVER increase years of experience.
10. Everything must remain factually correct.
11. NEVER remove important information from the resume.
12. Preserve all existing sections unless they are empty.
13. Preserve all contact information.
14. Preserve all links (GitHub, LinkedIn, Portfolio).

You MAY:

• Rewrite sentences professionally.
• Improve grammar.
• Improve ATS compatibility.
• Improve readability.
• Use stronger action verbs.
• Reorder existing skills.
• Reorder projects.
• Rewrite project descriptions.
• Rewrite experience descriptions.
• Add Job Description keywords ONLY if they genuinely describe existing experience.
• Naturally integrate important ATS keywords into existing bullet points.
• Prioritize keywords that appear multiple times in the Job Description.
• Avoid keyword stuffing or unnatural repetition.
• Optimize headings.
• Improve formatting.
• Use ATS-friendly section headings.
• Keep the resume in a clean single-column format.
• Maintain consistent bullet formatting.

Goal:

Produce a recruiter-level ATS optimized resume that maximizes keyword relevance, readability, recruiter appeal, and ATS parsing while remaining completely truthful.

Also explain every optimization clearly so the candidate understands why the ATS score improves.

Return ONLY valid JSON.

{{
    "optimized_resume":"",
    "summary":"",
    "keywords_added":[
        "",
        "",
        ""
    ],
    "keyword_count":0,
    "changes":[
        "",
        "",
        ""
    ],
    "keyword_mapping":[
        {{
            "jd_keyword":"",
            "resume_change":""
        }}
    ],
    "ats_improvements":[
        "",
        "",
        ""
    ],
    "sections_improved":[
        "",
        "",
        ""
    ],
    "predicted_improvement":"High",
    "compliance":{{
        "fake_skills":"No",
        "fake_projects":"No",
        "fake_experience":"No",
        "fake_certifications":"No",
        "ats_safe":"Yes"
    }}
}}
"""

    try:

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

    except Exception:

        return {

            "optimized_resume": resume_text,

            "summary":
                "AI resume optimization is temporarily unavailable because the AI quota has been reached. The original resume is shown.",

            "keywords_added": [],

            "keyword_count": 0,

            "changes": [
                "AI optimization temporarily unavailable."
            ],

            "keyword_mapping": [],

            "ats_improvements": [
                "Rule-based ATS analysis is still available."
            ],

            "sections_improved": [],

            "predicted_improvement": "Unavailable",

            "compliance": {

                "fake_skills": "No",
                "fake_projects": "No",
                "fake_experience": "No",
                "fake_certifications": "No",
                "ats_safe": "Yes"

            }

        }