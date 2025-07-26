from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_sections_by_relevance(sections, job_description):
    texts = [s['section_text'] for s in sections]
    vectorizer = TfidfVectorizer().fit_transform(texts + [job_description])
    vectors = vectorizer.toarray()
    job_vector = vectors[-1]
    section_vectors = vectors[:-1]
    scores = cosine_similarity([job_vector], section_vectors)[0]

    for i, score in enumerate(scores):
        sections[i]['relevance_score'] = float(score)
    ranked = sorted(sections, key=lambda x: -x['relevance_score'])
    for i, section in enumerate(ranked):
        section['importance_rank'] = i + 1
    return ranked
