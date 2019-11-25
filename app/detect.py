import cv2
from pytesseract import image_to_string


def load_image(image_path, flag=cv2.IMREAD_COLOR):
    try:
        image = cv2.imread(image_path, flag)
        return image
    except Exception as e:
        print('Unable to load image')


def preprocess_dilation(image_path):
    image = load_image(image_path, cv2.IMREAD_GRAYSCALE)
    # smooth the image to avoid noises
    image = cv2.medianBlur(image, 5)

    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
    thresh = cv2.dilate(thresh, None, iterations=10)
    thresh = cv2.erode(thresh, None, iterations=10)

    return thresh, thresh_color


def pytesseract_to_string(image_path):
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


def return_bounding_boxes(image_path, thresh, thresh_color):
    # For each contour, find the bounding rectangle and draw it
    # Find the contours
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(thresh_color, (x, y), (x+w, y+h), (0, 255, 0), 2)


# boxes = image_to_boxes(Image.open('test.PNG'))
# pytesseract_to_string('test.PNG')
# string = pytesseract_to_string('test.PNG')
contours_bounding_boxes('test.PNG')
