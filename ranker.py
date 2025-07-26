import re

def rank_sections_by_relevance(sections, metadata):
    persona = metadata["persona"].lower()
    task = metadata["job_to_be_done"].lower()
    keywords = (persona + " " + task).split()

    scored = []
    for section in sections:
        text = section["text"].lower()
        score = sum(text.count(word) for word in keywords)
        section["score"] = score
        scored.append(section)

    # Sort by score descending
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    return ranked
