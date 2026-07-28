
import re


def get_missing_keywords(resume_text, jd_text):

    resume_words = set(
        re.findall(
            r"[A-Za-z0-9+#.]+",
            resume_text.lower()
        )
    )

    jd_words = set(
        re.findall(
            r"[A-Za-z0-9+#.]+",
            jd_text.lower()
        )
    )

    ignore = {
        "the", "and", "for", "with", "from",
        "this", "that", "have", "will",
        "are", "was", "were", "your",
        "their", "our", "its", "into",
        "using", "used", "than", "also",
        "job", "role", "candidate"
    }

    missing = sorted(
        list(
            jd_words - resume_words - ignore
        )
    )

    return missing[:30]