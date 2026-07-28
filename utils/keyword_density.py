
import re
from collections import Counter


def keyword_density(resume_text):

    words = re.findall(
        r"[A-Za-z]+",
        resume_text.lower()
    )

    total = len(words)

    counter = Counter(words)

    density = {}

    for word, count in counter.items():

        density[word] = round(
            (count / total) * 100,
            2
        )

    return density