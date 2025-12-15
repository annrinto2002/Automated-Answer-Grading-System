import pdfplumber
import re

def extract_answers(pdf_path):
    answers_dict = {}
    
    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    # Regex to find numbered answers (e.g., 1. ..., 2. ..., 3. ...)
    pattern = re.compile(r'(\d+)\.\s(.*?)(?=\n\d+\.|\Z)', re.S)
    matches = pattern.findall(full_text)
    
    # Store in dictionary
    for num, answer in matches:
        answers_dict[int(num.strip())] = answer.strip().replace('\n', ' ')  # Clean up newlines inside answers
    
    return answers_dict

