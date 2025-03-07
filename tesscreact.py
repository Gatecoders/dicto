import pdfplumber
import pandas as pd
import re
import os

def extract_vocabulary_from_pdf(pdf_path, page_numbers=None):
    """
    Extract vocabulary words, meanings, and Hindi translations from a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        page_numbers: List of specific page numbers to extract (0-indexed). If None, extract all pages.
    
    Returns:
        DataFrame with columns: S.No., Word, Meaning, Hindi, Difficulty
    """
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # Determine which pages to process
        if page_numbers is None:
            pages_to_process = range(len(pdf.pages))
        else:
            pages_to_process = page_numbers
        
        for page_num in pages_to_process:
            if page_num >= len(pdf.pages):
                print(f"Warning: Page {page_num} does not exist in the PDF.")
                continue
                
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            # Process the text to extract vocabulary entries
            entries = process_page_text(text)
            all_data.extend(entries)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    return df

def process_page_text(text):
    """
    Process the text extracted from a PDF page to identify vocabulary entries.
    
    Args:
        text: Text extracted from a PDF page
    
    Returns:
        List of dictionaries containing the extracted data
    """
    lines = text.split('\n')
    entries = []
    current_entry = None
    
    # Pattern to match the start of a vocabulary entry (S.No. + Word)
    entry_pattern = re.compile(r'^(\d+)\s+([A-Z][a-z]+)\s+')
    
    for line in lines:
        line = line.strip()
        
        # Check if this line starts a new vocabulary entry
        match = entry_pattern.match(line)
        if match:
            # Save the previous entry if it exists
            if current_entry:
                entries.append(current_entry)
            
            # Start a new entry
            sno, word = match.groups()
            
            # Extract the meaning part (everything after the word)
            remaining_text = line[match.end():]
            
            current_entry = {
                'S.No.': sno,
                'Word': word,
                'Meaning': remaining_text,
                'Hindi': '',
                'Difficulty': ''
            }
        elif current_entry:
            # This line is a continuation of the current entry
            
            # Check if this line contains Hindi text
            # Hindi Unicode range: 0900-097F
            if any(0x0900 <= ord(c) <= 0x097F for c in line):
                # This line contains Hindi text
                hindi_match = re.search(r'([\u0900-\u097F\s]+)', line)
                if hindi_match:
                    current_entry['Hindi'] = hindi_match.group(1).strip()
                
                # Check if there's a difficulty number at the end
                difficulty_match = re.search(r'(\d+)$', line)
                if difficulty_match:
                    current_entry['Difficulty'] = difficulty_match.group(1)
            else:
                # This is likely a continuation of the meaning or other information
                # Append to the existing meaning
                current_entry['Meaning'] += " " + line
    
    # Add the last entry if it exists
    if current_entry:
        entries.append(current_entry)
    
    # Clean up the data
    for entry in entries:
        # Clean up meaning by removing Hindi text if it was accidentally included
        meaning = entry['Meaning']
        hindi_pattern = re.compile(r'[\u0900-\u097F]+')
        entry['Meaning'] = hindi_pattern.sub('', meaning).strip()
        
        # Remove difficulty number from meaning if present
        entry['Meaning'] = re.sub(r'\s+\d+$', '', entry['Meaning']).strip()
    
    return entries

def save_to_excel(df, output_path='vocabulary_list.xlsx'):
    """
    Save the extracted vocabulary to an Excel file.
    
    Args:
        df: DataFrame containing the vocabulary data
        output_path: Path where the Excel file should be saved
    """
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")

def save_to_csv(df, output_path='/Users/user/Desktop/vocabulary_list.csv'):
    """
    Save the extracted vocabulary to a CSV file.
    
    Args:
        df: DataFrame containing the vocabulary data
        output_path: Path where the CSV file should be saved
    """
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = "/Users/user/dicto/docs/blackbookV1.pdf"  # Replace with your actual PDF path
    
    # Extract data from specific pages (optional)
    # df = extract_vocabulary_from_pdf(pdf_path, page_numbers=[10, 11, 12])
    
    # Or extract from all pages
    df = extract_vocabulary_from_pdf(pdf_path)
    print(df)

    import pdb
    pdb.set_trace()
    # Save to Excel
    # save_to_excel(df)
    
    # Or save to CSV
    save_to_csv(df)