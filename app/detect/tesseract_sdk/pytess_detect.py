import os
import cv2
import pytesseract

# For Windows local environment
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'X:\Code\Tesseract-OCR\tesseract.exe'


def load_image(image_path, flag=cv2.IMREAD_COLOR):
    try:
        image = cv2.imread(image_path, flag)
        return image
    except Exception as e:
        print('Unable to load image', e)


def pytesseract_to_string(image_path):
    image = load_image(image_path)
    string = pytesseract.image_to_string(image)
    return string
