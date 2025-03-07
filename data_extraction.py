import re
from ocr import extract_text_from_pdf
def parse_text(text):
    pattern = r"(\d+)\s+([A-Za-z]+)\s+(.*)\s+([\u0900-\u097F]+)\s+(\d+)"  # Adjust regex as needed
    matches = re.findall(pattern, text)

    data = []
    for match in matches:
        import pdb
        pdb.set_trace()
        entry = {
            "id": int(match[0]),
            "word": match[1],
            "definition": match[2].strip(),
            "hindi_meaning": match[3],
            "score": int(match[4])
        }
        data.append(entry)
    return data

if __name__ == "__main__":
    pdf_path = "/Users/user/dicto/docs/blackbookV1.pdf"
    raw_text = extract_text_from_pdf(pdf_path)
    print(raw_text)
    import pdb
    pdb.set_trace()
    extracted_data = parse_text(raw_text)
    print(extracted_data)  # Check output before inserting into DB
