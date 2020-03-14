import cv2
# from nms import nms
import numpy as np
from pytesseract import image_to_string, image_to_data, Output
# Windows Env
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'X:\Code\Tesseract-OCR\tesseract.exe'


def load_image(image_path, flag=cv2.IMREAD_COLOR):
    try:
        image = cv2.imread(image_path, flag)
        return image
    except Exception as e:
        print('Unable to load image', e)


def pytesseract_to_string(image):
    string = image_to_string(image)
    return string


# def non_max_suppression(boxes, probs=None, overlapThresh=0.3):
#     boxes = np.asarray(boxes)
#     # if there are no boxes, return an empty list
#     if len(boxes) == 0:
#         return []

#     # if the bounding boxes are integers, convert them to floats -- this
#     # is important since we'll be doing a bunch of divisions
#     if boxes.dtype.kind == "i":
#         boxes = boxes.astype("float")

#     # initialize the list of picked indexes
#     pick = []

#     # grab the coordinates of the bounding boxes
#     x1 = boxes[:, 0]
#     y1 = boxes[:, 1]
#     x2 = boxes[:, 2]
#     y2 = boxes[:, 3]

#     # compute the area of the bounding boxes and grab the indexes to sort
#     # (in the case that no probabilities are provided, simply sort on the
#     # bottom-left y-coordinate)
#     area = (x2 - x1 + 1) * (y2 - y1 + 1)
#     idxs = y2

#     # if probabilities are provided, sort on them instead
#     if probs is not None:
#         idxs = probs

#     # sort the indexes
#     idxs = np.argsort(idxs)

#     # keep looping while some indexes still remain in the indexes list
#     while len(idxs) > 0:
#         # grab the last index in the indexes list and add the index value
#         # to the list of picked indexes
#         last = len(idxs) - 1
#         i = idxs[last]
#         pick.append(i)

#         # find the largest (x, y) coordinates for the start of the bounding
#         # box and the smallest (x, y) coordinates for the end of the bounding
#         # box
#         xx1 = np.maximum(x1[i], x1[idxs[:last]])
#         yy1 = np.maximum(y1[i], y1[idxs[:last]])
#         xx2 = np.minimum(x2[i], x2[idxs[:last]])
#         yy2 = np.minimum(y2[i], y2[idxs[:last]])

#         # compute the width and height of the bounding box
#         w = np.maximum(0, xx2 - xx1 + 1)
#         h = np.maximum(0, yy2 - yy1 + 1)

#         # compute the ratio of overlap
#         overlap = (w * h) / area[idxs[:last]]

#         # delete all indexes from the index list that have overlap greater
#         # than the provided overlap threshold
#         idxs = np.delete(idxs, np.concatenate(([last],
#             np.where(overlap > overlapThresh)[0])))

#     # return only the bounding boxes that were picked
#     return boxes[pick].astype("int")


def pytesseract_to_boxes(image):
    d = image_to_data(image, output_type=Output.DICT)
    n_boxes = len(d['level'])
    n_scores = len(d['conf'])

    boxes = []
    confidences = []

    for i in range(n_boxes):
        confidences.append(int(d['conf'][i]))
        boxes.append((d['left'][i], d['top'][i], d['width'][i], d['height'][i]))
        # confidence_with_box[confidence] = (x, y, w, h)
        # print(confidence)

        # cv2.rectangle(image, (d['left'][i], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
    print(len(boxes))
    # indices = nms.boxes(boxes, confidences, nms_algorithm=nms.fast.nms)
    # new_boxes = non_max_suppression_fast(boxes, 0.5, confidences)
    # indices = np.array(indices).reshape(-1)
    # print(len(indices))
    # drawrects = np.array(boxes)[indices]
    newer_boxes = non_max_suppression(boxes, confidences, 0.3)
    print(len(newer_boxes))

    for rect in newer_boxes:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

    # for key, value in confidence_with_box.items():
         # print(key, value)
        # cv2.rectangle(image, (value[0], value[1]), (value[0] + value[2], value[1] + value[3]), (0, 255, 0), 2)
        # crop_img = image[value[1]:value[1] + value[3], value[0]:value[0] + value[2]]
        # print(pytesseract_to_string(crop_img))

    cv2.imshow('image', image)
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
    # bla bla
    results = {}
    bounding_boxes_coords = []
    detected_strings = []
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        bounding_boxes_coords.append(cv2.boundingRect(cnt))


    for box in bounding_boxes_coords:
        # print(box, '\n', dir(box))
        # print(box[0], box[1], box[2], box[3])
        cv2.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
        crop_img = image[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        detected_strings.append(pytesseract_to_string(crop_img))
        print(pytesseract_to_string(crop_img))
        cv2.imshow("cropped", crop_img)
        cv2.waitKey()


def mser(image):
    mser = cv2.MSER_create()
    # img = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
    regions, bboxes = mser.detectRegions(image)
    for box in bboxes:
        # print(box, '\n', dir(box))
        # print(box[0], box[1], box[2], box[3])
        cv2.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), -1)

    cv2.imshow('wew', image)
    cv2.waitKey()


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

# image = load_image('test2.PNG')
# print(pytesseract_to_string(image))
# tresh = preprocess_dilation(image)
# return_bounding_boxes(image, tresh)


# pytesseract_to_boxes(image)