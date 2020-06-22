import time
import ntpath
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

# Variables to your Microsoft Computer Vision Account
# Make sure not to make public those variables! ( Very important! Don't make it public on GitHub, etc. )
subscription_key = "..."  # Place your subscription key here
endpoint = "..."          # Place your endpoint here
simple_headers = {'Ocp-Apim-Subscription-Key': subscription_key}
headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}

# -NOT USED- Additional info endpoint, like faces, objects, people, etc. 
analyze_url = endpoint + "vision/v3.0/analyze"
# Text based endpoint, gives greater accuracy, for documents, etc.
text_url = endpoint + "/vision/v3.0/read/analyze"
# OCR based endpoint, is faser and still gives good results
ocr_url = endpoint + "vision/v3.0/ocr"
ocr_params = {'language': 'unk', 'detectOrientation': 'true'}


def load_raw_image(image_path):
    # Load raw image file into memory
    with open(image_path, 'rb') as f:
        img = f.read()
        return img
    return None


def get_image_sizes(image_path):
    im = Image.open(image_path)
    width, height = im.size
    return width, height


# The 'results' object contains various fields that describe the text found on the image, 
# as well as the granular text and associated boxes.
def ms_ocr_image_api(url, params, headers, image_data):
    response = requests.post(url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    results = response.json()
    return results


# The 'results' object contains various fields that describe the regions of text
# found on the image, alongisde the lines of text found. Also has bounding boxes for regions/lines.
# Extracting text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.
# Holds the URI used to retrieve the recognized text.
# operation_url = response.headers["Operation-Location"]
# The recognized text isn't immediately available, so poll to wait for completion.
def ms_recognize_text_api(url, headers, image_data):
    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()

    poll = True
    final_results = {}
    while poll:
        response_final = requests.get(response.headers["Operation-Location"], headers=simple_headers)
        final_results = response_final.json()
        time.sleep(1)
        if ("analyzeResult" in final_results):
            poll = False
        if ("status" in final_results and final_results['status'] == 'failed'):
            poll = False

    return final_results


# The advanced mode can recognize handwritten text, and more.
def analyze_image(image_path, advanced_mode=False):
    # Load the image from the image path
    image_data = load_raw_image(image_path)
    image_name = ntpath.basename(image_path)

    if not advanced_mode:
        # Results from the Microsoft Computer Vision OCR API
        # Extract the words, their bounding boxes and overall text.
        ocr_results = ms_ocr_image_api(ocr_url, ocr_params, headers, image_data)
        overall_text, texts_and_boxes = analyze_ocr_results(ocr_results)
    elif advanced_mode:
        # Advanced results from the Microsoft Computer Vision Document OCR API
        # Extract the lines, their bounding boxes and overall text.
        lines_results = ms_recognize_text_api(text_url, headers, image_data)
        overall_text, texts_and_boxes = analyze_text_results(lines_results)

    texts = [text[0] for text in texts_and_boxes]
    # Draw partial results
    draw_resulted_images(texts_and_boxes, image_data, image_path, image_name, 'partial', advanced_mode)
    return overall_text, texts, texts_and_boxes


# Overlay the image with the extracted text and boxes
def draw_resulted_images(text_and_boxes, image_data, image_path, image_name, mode='partial', advanced_mode=False):
    if mode == 'partial':
        if advanced_mode:
            draw_texts_and_boxes(text_and_boxes, image_data, image_path, draw_text=False, new_image_name='granular_partial_' + image_name)
        else:
            draw_words_and_boxes(text_and_boxes, image_data, image_path, draw_text=False, new_image_name='granular_partial_' + image_name)
    else:
        # Load the image from the image path
        image_data = load_raw_image(image_path)
        if advanced_mode:
            draw_texts_and_boxes(text_and_boxes, image_data, image_path, new_image_name='granular_translated_' + image_name)
        else:
            draw_words_and_boxes(text_and_boxes, image_data, image_path, new_image_name='granular_translated_' + image_name)    


# Extract the recognized text lines, with bounding boxes.
def analyze_text_results(results):
    line_data = []
    overall_text = ""

    if "analyzeResult" in results:
        line_data = [(line["text"], line["boundingBox"])
                     for line in results["analyzeResult"]["readResults"][0]["lines"]]
        for line in line_data:
            overall_text += line[0] + '\n'

    return overall_text, line_data


# Extract the recognized words, with bounding boxes, as well as the overall text.
def analyze_ocr_results(results):
    line_infos = [region["lines"] for region in results["regions"]]
    word_data = []
    overall_text = ""

    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                bbox = [int(coord) for coord in word_info["boundingBox"].split(",")]
                text = word_info["text"]
                overall_text += text + ' '
                word_data.append([text, bbox])
            overall_text += '\n'

    return overall_text, word_data


# Draw words and their associated boxes.
def draw_words_and_boxes(words_and_boxes_data, image_data, image_path, new_image_name, draw_text=True):
    ax, font_size = prepare_plot(image_data, image_path)

    for data in words_and_boxes_data:
        word, bbox = data[0], data[1]
        origin = [bbox[0], bbox[1]]
        draw_rectangle_box(ax, *origin, bbox[2], bbox[3])
        if draw_text:
            draw_text_annotations(word, *origin, abs(bbox[2] - bbox[0]), font_size)

    save_and_clear(new_image_name)


# Draw lines of text and their associated boxes ( polygons in this case, for more accurate results ).
def draw_texts_and_boxes(lines_and_boxes_data, image_data, image_path, new_image_name, draw_text=True):
    ax, font_size = prepare_plot(image_data, image_path)

    for data in lines_and_boxes_data:
        text = data[0]
        vertices = [(data[1][i], data[1][i + 1])
                    for i in range(0, len(data[1]), 2)]
        draw_polygon_box(ax, vertices)
        if draw_text:
            box_width = vertices[1][0] - vertices[0][0]
            draw_text_annotations(text, vertices[0][0], vertices[0][1], box_width, font_size)

    save_and_clear(new_image_name)


def draw_polygon_box(ax, vertices):
    patch = Polygon(vertices, closed=True, fill=True, linewidth=2, alpha=0.4, color='y')
    ax.axes.add_patch(patch)


def draw_rectangle_box(ax, upleft_x, upleft_y, botright_x, botright_y):
    patch = Rectangle((upleft_x, upleft_y), botright_x, botright_y, alpha=0.4,
                      fill=True, linewidth=1, color='lightskyblue')
    ax.axes.add_patch(patch)


def draw_text_annotations(text, text_origin_x, text_origin_y, box_width, font_size=12):
    plt.text(text_origin_x, text_origin_y - 5, '{:s}'.format(text),
             bbox=dict(facecolor='green', alpha=0.5),
             fontsize=font_size, color='white', weight='bold')


def prepare_plot(image_data, image_path):
    dpi = 100
    img_width, img_height = get_image_sizes(image_path)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(img_width / dpi * 2, img_height / dpi)
    if img_width >= 1300:
        font_size = int((img_width * 8) / 1200)
    elif 500 <= img_width < 1300:
        font_size = int((img_width * 12) / 1200)
    else:
        font_size = int((img_width * 24) / 1200) 

    image = Image.open(BytesIO(image_data))
    ax = plt.imshow(image)
    return ax, font_size


def save_and_clear(new_image_name):
    new_image_path = r'.\\static\\results\\' + new_image_name
    plt.axis('off')
    plt.savefig(new_image_path, bbox_inches='tight', pad_inches=0)
    plt.clf()
