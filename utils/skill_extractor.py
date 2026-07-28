
import re

# --------------------------------------------------
# Master Skill List
# --------------------------------------------------
MASTER_SKILLS = [

    # Programming Languages
    "Python", "Java", "C", "C++", "C#", "JavaScript",
    "TypeScript", "Go", "Rust", "Kotlin", "Swift",
    "PHP", "R", "MATLAB", "Scala", "Dart",

    # Frontend
    "HTML", "CSS", "Bootstrap", "Tailwind CSS",
    "React", "Next.js", "Angular", "Vue",
    "Svelte", "Redux", "Material UI",

    # Backend
    "Node.js", "Express", "Flask", "Django",
    "FastAPI", "Spring Boot", "ASP.NET",
    "REST API", "GraphQL",

    # Mobile
    "Android", "Flutter", "React Native",
    "Firebase",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "Oracle",
    "MongoDB", "SQLite", "Redis",
    "Cassandra", "DynamoDB",

    # Cloud
    "AWS", "Azure", "Google Cloud",
    "GCP", "Firebase",
    "CloudFormation", "Terraform",

    # DevOps
    "Docker", "Kubernetes", "Git",
    "GitHub", "GitLab", "Bitbucket",
    "Jenkins", "CI/CD", "Ansible",

    # AI / ML
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "Scikit-learn",
    "OpenCV",
    "NLP",
    "LLM",
    "Generative AI",
    "LangChain",
    "RAG",
    "FAISS",
    "Pinecone",
    "Qdrant",
    "HuggingFace",

    # Data Science
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Power BI",
    "Excel",
    "Tableau",

    # Cybersecurity
    "Linux",
    "Networking",
    "Cyber Security",
    "Ethical Hacking",
    "OWASP",

    # Testing
    "JUnit",
    "PyTest",
    "Selenium",
    "Postman",

    # Software Engineering
    "OOP",
    "Data Structures",
    "Algorithms",
    "Operating Systems",
    "DBMS",
    "Computer Networks",
    "System Design",

    # Soft Skills
    "Leadership",
    "Communication",
    "Problem Solving",
    "Teamwork",
    "Critical Thinking"
]
SKILL_PRIORITY = {
    "Python": 5,
    "Java": 5,
    "C++": 5,
    "SQL": 5,

    "React": 4,
    "Node.js": 4,
    "AWS": 4,
    "Docker": 4,
    "Kubernetes": 4,
    "Machine Learning": 4,

    "Git": 3,
    "GitHub": 3,
    "Firebase": 3,
    "MongoDB": 3,
    "PostgreSQL": 3,
    "Flask": 3,
    "Django": 3,
    "FastAPI": 3,

    "HTML": 2,
    "CSS": 2,
    "Excel": 2,
    "Linux": 2
}


def extract_skills(text):

    if not text:
        return []

    found = []

    for skill in MASTER_SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text.lower()):
            found.append(skill)

    return sorted(set(found))


def compare_skills(resume_text, jd_text):

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    return {
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "matched": matched,
        "missing": missing
    }