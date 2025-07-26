import os
import json
import time
from pathlib import Path
from extract_outline import extract_outline_and_sections
from relevance import rank_sections_by_relevance
from generator import build_output_json

INPUT_DIR = "input"
OUTPUT_DIR = "output"
PERSONA = "Travel Planner"
TASK = "Plan a trip of 4 days for a group of 10 college friends."

def main():
    print("="*60)
    print("🏁 Persona-Aware Document Summarization - Offline Edition")
    print("="*60)

    input_path = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        print("⚠️  No PDF files found in /input folder.")
        return

    for pdf_file in pdf_files:
        print(f"\n📄 Processing: {pdf_file.name}")
        start_time = time.time()

        try:
            title, sections = extract_outline_and_sections(pdf_file)
            print(f"   📑 Title: {title}")
            print(f"   ✂️  Found {len(sections)} sections")

            ranked_sections = rank_sections_by_relevance(sections, TASK)
            final_output = build_output_json([pdf_file.name], PERSONA, TASK, ranked_sections)

            out_path = output_path / f"{pdf_file.stem}_summary.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(final_output, f, indent=2, ensure_ascii=False)

            elapsed = time.time() - start_time
            print(f"   ✅ Done! Saved to {out_path.name} in {elapsed:.2f}s")

        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")

if __name__ == "__main__":
    main()
