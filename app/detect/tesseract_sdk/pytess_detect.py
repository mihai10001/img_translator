import cv2
from pytesseract import image_to_string
# Windows Env
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'X:\Code\Tesseract-OCR\tesseract.exe'


def load_image(image_path, flag=cv2.IMREAD_COLOR):
    try:
        image = cv2.imread(image_path, flag)
        return image
    except Exception as e:
        print('Unable to load image', e)


def pytesseract_to_string(image_path):
    image = load_image(image_path)
    string = image_to_string(image)
    return string