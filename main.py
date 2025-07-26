# main.py
from pdf_parser import extract_all_sections
from ranker import rank_sections_by_relevance
from generator import generate_final_output

def main():
    input_file = "input/input.json"
    intermediate_file = "intermediate/intermediate.json"
    output_file = "output/challenge1b_output.json"

    print("🔍 Extracting content from PDFs...")
    all_sections, metadata = extract_all_sections(input_file)

    print("📊 Ranking sections...")
    ranked_sections = rank_sections_by_relevance(all_sections, metadata)

    print("💾 Generating output...")
    generate_final_output(metadata, ranked_sections, intermediate_file, output_file)

    print("✅ All done! Check:", output_file)

if __name__ == "__main__":
    main()
