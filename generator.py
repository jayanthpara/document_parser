from datetime import datetime
from summarizer import summarize_text

def build_output_json(documents, persona, job, ranked_sections):
    top_sections = ranked_sections[:5]
    return {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": sec["section_title"],
                "importance_rank": sec["importance_rank"],
                "page_number": sec["page_number"]
            } for sec in top_sections
        ],
        "subsection_analysis": [
            {
                "document": sec["document"],
                "refined_text": summarize_text(sec["section_text"]),
                "page_number": sec["page_number"]
            } for sec in top_sections
        ]
    }
