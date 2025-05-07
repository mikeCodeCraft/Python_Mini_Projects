import pytesseract
import os 
from PIL import Image
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert():
    img = Image.open('Screenshot (113).png')
    text = pytesseract.image_to_string(img)
    print(text)
    
convert()