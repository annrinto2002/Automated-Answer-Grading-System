import re
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def main(image_path):
    # Open the image
    image = Image.open(image_path)

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(image)

    # Define a regex pattern to capture question numbers and their corresponding answers
    pattern = r"(\d+)\.\s+([^\n]+)"

    # Find all matches and convert them into a dictionary
    extracted_answers = {int(match[0]): match[1].strip() for match in re.findall(pattern, extracted_text)}
    print(extracted_answers)
    return extracted_answers


img = "C:/Users/Admin/Downloads/Lorem Ipsum_page-0001.jpg"
main(img)