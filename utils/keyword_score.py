
import re
from collections import Counter


def calculate_keyword_score(resume_text, jd_text):

    resume = resume_text.lower()
    jd = jd_text.lower()

    stop_words = {
        "the", "and", "for", "with", "this", "that",
        "are", "you", "your", "our", "their", "will",
        "have", "has", "from", "into", "using", "use",
        "should", "must", "can", "job", "role",
        "candidate", "required", "preferred",
        "skills", "skill", "experience",
        "knowledge", "ability", "working",
        "strong", "good", "excellent",
        "responsible", "responsibilities",
        "looking", "ability", "preferred",
        "qualification", "qualifications"
    }

    words = re.findall(
        r"[A-Za-z][A-Za-z0-9+#.\-]{2,}",
        jd
    )

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    frequency = Counter(words)

    total_weight = sum(frequency.values())

    matched_weight = 0

    matched_keywords = []
    missing_keywords = []

    for keyword, weight in frequency.items():

        if keyword in resume:

            matched_weight += weight

            matched_keywords.append({
                "keyword": keyword,
                "weight": weight
            })

        else:

            missing_keywords.append({
                "keyword": keyword,
                "weight": weight
            })

    if total_weight == 0:
        score = 0

    else:
        score = (matched_weight / total_weight) * 100

    matched_keywords = sorted(
        matched_keywords,
        key=lambda x: x["weight"],
        reverse=True
    )

    missing_keywords = sorted(
        missing_keywords,
        key=lambda x: x["weight"],
        reverse=True
    )

    return {
        "score": round(score, 2),

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,

        "matched_count": len(matched_keywords),

        "missing_count": len(missing_keywords),

        "total_keywords": len(frequency),

        "weighted_match": matched_weight,

        "weighted_total": total_weight
    }