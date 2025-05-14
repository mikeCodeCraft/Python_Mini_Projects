import cv2
import pytesseract
import json

# Optional: Set path to tesseract.exe if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the answer key
with open('answer_key.json') as f:
    answer_key = json.load(f)

# Load and preprocess image
img = cv2.imread('sample.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY_INV, 15, 10)

# OCR with bounding box
custom_config = r'--oem 3 --psm 6'
ocr_result = pytesseract.image_to_data(thresh, config=custom_config, output_type=pytesseract.Output.DICT)

# Extract answers
detected_answers = {}
for i in range(len(ocr_result['text'])):
    word = ocr_result['text'][i].strip()
    if word in ['A', 'B', 'C', 'D']:
        # Get nearby text that could be a question number
        x, y, w, h = ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]
        for j in range(i-3, i+3):
            if 0 <= j < len(ocr_result['text']):
                near_text = ocr_result['text'][j].strip().replace('.', '')
                if near_text.isdigit():
                    detected_answers[near_text] = word
                    break

# Compare with answer key
score = 0
print("\nResult:")
for q, correct_ans in answer_key.items():
    detected = detected_answers.get(q, "Not Found")
    result = "Correct" if detected == correct_ans else "Wrong"
    print(f"Q{q}: Detected = {detected}, Expected = {correct_ans} => {result}")
    if result == "Correct":
        score += 1

print(f"\nFinal Score: {score}/{len(answer_key)}")