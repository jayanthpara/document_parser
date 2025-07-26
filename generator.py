import json

def generate_final_output(metadata, ranked_sections, intermediate_path, output_path):
    # Save intermediate
    with open(intermediate_path, 'w') as f:
        json.dump(ranked_sections, f, indent=2)

    # Select top 5
    top5 = ranked_sections[:5]

    extracted_sections = []
    subsection_analysis = []

    for i, sec in enumerate(top5, 1):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": i,
            "page_number": sec["page_number"]
        })
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": sec["text"][:2000],  # cap text
            "page_number": sec["page_number"]
        })

    final = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_path, 'w') as f:
        json.dump(final, f, indent=2)
