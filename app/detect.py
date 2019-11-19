import cv2
from pytesseract import Output, image_to_string, image_to_data


def load_image(image_path):
    try:
        image = cv2.imread(image_path)
        return image
    except Exception as e:
        print('Unable to load image')


def pytesseract_to_string(image_path):
    image = load_image(image_path)
    string = image_to_string(image)
    return string


def pytesseract_to_boxes(image_path):
    image = load_image(image_path)
    info_dict = image_to_data(image, output_type=Output.DICT,  config='--oem 3 --psm 6')
    box_number = len(info_dict['level'])

    for i in range(box_number):
        (x, y, w, h) = (info_dict['left'][i], info_dict['top'][i], info_dict['width'][i], info_dict['height'][i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('wew', image)
    cv2.waitKey()
    # return string

# boxes = image_to_boxes(Image.open('test.PNG'))
# pytesseract_to_string('test.PNG')
pytesseract_to_boxes('test.PNG')
