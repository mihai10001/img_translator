import cv2
from pytesseract import image_to_string


def load_image(image_path, flag=cv2.IMREAD_COLOR):
    try:
        image = cv2.imread(image_path, flag)
        return image
    except Exception as e:
        print('Unable to load image')


def pytesseract_to_string(image_path, ):
    image = load_image(image_path)
    string = image_to_string(image)
    return string


# def pytesseract_to_boxes(image_path):
#     image = load_image(image_path)
#     info_dict = image_to_data(image, output_type=Output.DICT,  config='--oem 3 --psm 6')
#     box_number = len(info_dict['level'])

#     for i in range(box_number):
#         (x, y, w, h) = (info_dict['left'][i], info_dict['top'][i], info_dict['width'][i], info_dict['height'][i])
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     cv2.imshow('wew', image)
#     cv2.waitKey()
    # return string


def return_bounding_boxes(image_path):
    image = load_image(image_path, cv2.IMREAD_GRAYSCALE)
    cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU, image)

    contours, hier = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        # draw a white rectangle to visualize the bounding rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.drawContours(image, contours, -1, (255, 255, 0), 1)
    cv2.imshow('wew', image)
    cv2.waitKey()


# boxes = image_to_boxes(Image.open('test.PNG'))
# pytesseract_to_string('test.PNG')
# string = pytesseract_to_string('test.PNG')
contours_bounding_boxes('test.PNG')
