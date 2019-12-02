import cv2
from pytesseract import image_to_string, image_to_data, Output


def load_image(image_path, flag=cv2.IMREAD_COLOR):
    try:
        image = cv2.imread(image_path, flag)
        return image
    except Exception as e:
        print('Unable to load image')


def pytesseract_to_string(image):
    string = image_to_string(image)
    return string


def pytesseract_to_boxes(img):
    d = image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)


def preprocess_dilation(image, iterations_count=20):
    # Transform the image to grayscale, then apply a slight blur transformation
    # (or any smooth operations), in order to eliminate some noise
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray_noiseless = cv2.medianBlur(image_gray, 5)

    # Apply adaptive threshold, in order to empah
    thresh = cv2.adaptiveThreshold(image_gray_noiseless, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 1, 11, 2)

    # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
    thresh = cv2.dilate(thresh, None, iterations=iterations_count)
    thresh = cv2.erode(thresh, None, iterations=iterations_count)

    return thresh


def return_bounding_boxes(image, thresh):
    # For each contour, find the bounding rectangle and draw it
    # Find the contours
    bounding_boxes_coords = []
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        bounding_boxes_coords.append(cv2.boundingRect(cnt))
        # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for box in bounding_boxes_coords:
        crop_img = image[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
        print(pytesseract_to_string(crop_img))
        cv2.imshow("cropped", crop_img)
        cv2.waitKey()

    # cv2.imshow('wew', image)
    # cv2.waitKey()


# def pytesseract_to_boxes(image_path):
#     image = load_image(image_path)
#     info_dict = image_to_data(image, output_type=Output.DICT,  config='--oem 3 --psm 6')
#     box_number = len(info_dict['level'])

#     for i in range(box_number):
#         (x, y, w, h) = (info_dict['left'][i], info_dict['top'][i], info_dict['width'][i], info_dict['height'][i])
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     cv2.imshow('wew', image)
#     cv2.waitKey()
#     return string

image = load_image('test.PNG')
# tresh = preprocess_dilation(image)
pytesseract_to_boxes(image)
# return_bounding_boxes(image, tresh)
