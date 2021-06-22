import ntpath
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from google.cloud import vision
from google.oauth2 import service_account

# Path to your Google Vision Account Token
# Make sure not to make public your Token! ( Very important! Don't make it public on GitHub, etc. )
credentials = service_account.Credentials.from_service_account_file(r'.\\env\\GoogleServiceAccountToken.json')


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
def google_ocr_image_api(image_path):
    client = vision.ImageAnnotatorClient(credentials=credentials)
    content = load_raw_image(image_path)
    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        ex = Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        print(ex)
        return None

    return response.text_annotations


# The 'results' object contains various fields that describe the regions of text
# found in the 'document', handwriten text as well as diacritics.
def google_ocr_doc_api(image_path):
    client = vision.ImageAnnotatorClient(credentials=credentials)
    content = load_raw_image(image_path)
    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    if response.error.message:
        ex = Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        print(ex)
        return None

    return response.full_text_annotation


# The advanced mode can recognize handwritten text, and more.
def analyze_image(image_path, advanced_mode=False):
    # Load the image from the image path
    image_data = load_raw_image(image_path)
    image_name = ntpath.basename(image_path)

    if not advanced_mode:
        # Results from the Google Vision OCR API
        # Extract the words, their bounding boxes and overall text.
        ocr_results = google_ocr_image_api(image_path)
        overall_text = ocr_results[0].description
        words_and_boxes = analyze_ocr_results(ocr_results[1:])
    elif advanced_mode:
        # Advanced results from the Google Vision Documents OCR API
        # Extract the words, their bounding boxes and overall text.
        ocr_results = google_ocr_doc_api(image_path)
        overall_text = ocr_results.text
        words_and_boxes = analyze_handwrite_results(ocr_results)

    words = [word_box[0] for word_box in words_and_boxes]
    # Draw partial results
    draw_resulted_images(words_and_boxes, image_data, image_path, image_name)
    return overall_text, words, words_and_boxes


# Extract the recognized words and their bounding boxes.
def analyze_ocr_results(results):
    word_data = []

    for text in results:
        vertices = text.bounding_poly.vertices
        bbox = [vertices[0].x, vertices[0].y, vertices[2].x, vertices[2].y]
        this_box = [text.description, bbox]
        word_data.append(this_box)

    return word_data


def analyze_handwrite_results(results):
    word_data = []

    for page in results.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                print("Paragrpah:", paragraph)
                for word in paragraph.words:
                    vertices = word.bounding_box.vertices
                    bbox = [vertices[0].x, vertices[0].y, vertices[2].x, vertices[2].y]
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    this_box = [word_text, bbox]
                    word_data.append(this_box)

    return word_data


# Overlay the image with the extracted text and boxes
def draw_resulted_images(words_and_boxes, image_data, image_path, image_name, mode='partial'):
    if mode == 'partial':
        draw_words_and_boxes(words_and_boxes, image_data, image_path, draw_text=False, new_image_name='granular_partial_' + image_name)
    else:
        # Load the image from the image path
        image_data = load_raw_image(image_path)
        draw_words_and_boxes(words_and_boxes, image_data, image_path, new_image_name='granular_translated_' + image_name)


# Draw words and their associated boxes.
def draw_words_and_boxes(words_and_boxes_data, image_data, image_path, new_image_name, draw_text=True):
    ax, font_size = prepare_plot(image_data, image_path)

    for data in words_and_boxes_data:
        word, bbox = data[0], data[1]
        origin = [bbox[0], bbox[1]]
        draw_rectangle_box(ax, *origin, bbox[2] - bbox[0], bbox[3] - bbox[1])
        if draw_text:
            draw_text_annotations(word, *origin, font_size)

    save_and_clear(new_image_name)


def draw_rectangle_box(ax, upleft_x, upleft_y, botright_x, botright_y):
    patch = Rectangle((upleft_x, upleft_y), botright_x, botright_y, alpha=0.4,
                      fill=True, linewidth=1, color='lightskyblue')
    ax.axes.add_patch(patch)


def draw_text_annotations(text, text_origin_x, text_origin_y, font_size=12):
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
