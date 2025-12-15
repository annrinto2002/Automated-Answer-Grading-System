import cv2
import pytesseract
import re

# Set path to Tesseract-OCR if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_answers(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to remove noise
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Extract text using Tesseract
    extracted_text = pytesseract.image_to_string(thresh)

    # Clean and structure extracted text into a dictionary
    answers = {}
    lines = extracted_text.split("\n")
    
    for line in lines:
        match = re.match(r"(\d+)\.?\s*(.*)", line.strip())  # Match question number and answer
        if match:
            q_num, answer = match.groups()
            answers[int(q_num)] = answer.strip()
    print(answers)
    return answers

# Example usage
img = "C:/Users/Admin/Downloads/111.jpg"
extract_answers(img)