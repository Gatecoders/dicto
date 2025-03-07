import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    print(text)
    import pdb
    pdb.set_trace()
    return clean_text(text)

def clean_text(text):
    # Remove unwanted encoding artifacts like (cid:xxx)
    text = re.sub(r"\(cid:\d+\)", "", text)  
    text = re.sub(r"©.*", "", text)  # Remove copyright notice

    # Replace multiple newlines with a single space to fix broken words
    text = text.replace("\n", " ")

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text