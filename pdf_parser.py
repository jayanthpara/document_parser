import fitz  # PyMuPDF
import json
import os
from datetime import datetime

def extract_sections_from_pdf(pdf_path, title):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if len(text.strip()) == 0:
            continue
        sections.append({
            "document": os.path.basename(pdf_path),
            "section_title": title,  # fallback title
            "page_number": page_num,
            "text": text.strip()
        })
    return sections

def extract_all_sections(input_json_path):
    with open(input_json_path, 'r') as f:
        input_data = json.load(f)

    documents = input_data["documents"]
    persona = input_data["persona"]["role"]
    job = input_data["job_to_be_done"]["task"]

    all_sections = []
    for doc in documents:
        path = os.path.join("input", doc["filename"])
        sections = extract_sections_from_pdf(path, doc["title"])
        all_sections.extend(sections)

    metadata = {
        "input_documents": [doc["filename"] for doc in documents],
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": str(datetime.now())
    }

    return all_sections, metadata
