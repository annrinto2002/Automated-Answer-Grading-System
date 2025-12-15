import easyocr
import cv2
import numpy as np
import re

def preprocess_image(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding (better for handwritten text)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)

    # Optional: Apply morphological operations to reduce noise
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)

    return processed

def extract_answers(image_path):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Preprocess the image
    processed_img = preprocess_image(image_path)

    # Perform OCR
    results = reader.readtext(processed_img)

    # Extract text and structure into dictionary
    answers = {}
    for (bbox, text, prob) in results:
        text = text.strip()
        match = re.match(r"(\d+)\.?\s*(.*)", text)  # Match "number. answer"
        if match:
            q_num, answer = match.groups()
            answers[int(q_num)] = answer.strip()

    return answers

# Example usage

image_path = "F:/2025/Rajagiri/AAGS/aagsApp/static/media/answerSheet/WhatsApp_Image_2025-03-03_at_10_AZupg8Q.23.29_97079d70.jpg"
extracted_answers = extract_answers(image_path)
print(extracted_answers)
