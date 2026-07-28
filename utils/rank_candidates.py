
from sklearn.metrics.pairwise import cosine_similarity

from utils.embeddings import get_embedding


def rank_candidates(job_description, resumes):

    jd_embedding = get_embedding(job_description)

    rankings = []

    for resume in resumes:

        name = resume["name"]
        text = resume["text"]

        resume_embedding = get_embedding(text)

        similarity = cosine_similarity(
            [jd_embedding],
            [resume_embedding]
        )[0][0]

        score = round(float(similarity * 100), 2)

        rankings.append(
            {
                "name": name,
                "text": text,
                "score": score
            }
        )

    rankings.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return rankings