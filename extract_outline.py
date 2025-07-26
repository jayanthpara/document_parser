import fitz  # PyMuPDF
import re
from collections import Counter

def extract_title_from_document(doc):
    metadata_title = doc.metadata.get('title', '').strip()
    if metadata_title and 5 <= len(metadata_title) <= 100:
        return metadata_title
    return "Untitled Document"

def is_likely_heading(text, font_size, is_bold, body_font_size):
    if not text or len(text) < 5 or len(text.split()) > 15:
        return False
    if font_size > body_font_size + 2 or is_bold:
        return True
    return False

def extract_outline_and_sections(pdf_path):
    doc = fitz.open(pdf_path)
    title = extract_title_from_document(doc)

    font_sizes = []
    sections = []
    page_texts = [page.get_text() for page in doc]

    # Analyze font sizes
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    font_sizes.append(span["size"])

    body_font_size = Counter(font_sizes).most_common(1)[0][0] if font_sizes else 12

    # Detect headings and collect sections
    headings = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                max_font = 0
                is_bold = False
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        line_text += text + " "
                        max_font = max(max_font, span["size"])
                        if "bold" in span.get("font", "").lower() or span.get("flags", 0) & 2**4:
                            is_bold = True
                line_text = line_text.strip()
                if is_likely_heading(line_text, max_font, is_bold, body_font_size):
                    headings.append({
                        "text": line_text,
                        "page": page_num,
                        "font_size": max_font,
                        "is_bold": is_bold
                    })

    # Sort by page and offset
    headings = sorted(headings, key=lambda h: (h["page"]))

    # Now collect text between headings
    sections = []
    for i in range(len(headings)):
        start_page = headings[i]["page"] - 1
        end_page = headings[i+1]["page"] - 1 if i+1 < len(headings) else len(doc)
        section_text = ""
        for p in range(start_page, end_page):
            section_text += doc[p].get_text() + "\n"
        sections.append({
            "document": pdf_path.name,
            "section_title": headings[i]["text"],
            "page_number": headings[i]["page"],
            "section_text": section_text.strip()
        })

    doc.close()

    return title, sections
