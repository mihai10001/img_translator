import os
import json
import datetime
from PIL import Image
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename

from language.language_options import apply_options, possible_lang_options, get_country_language

from detect.detection_methods import possible_detection_methods
from detect.abbyy_api.abbyy_vision_api import abbyy_to_string
from detect.tesseract_sdk.pytess_detect import pytesseract_to_string
from detect.google_api.google_vision_api import analyze_image as g_analyze, draw_resulted_images as g_draw_results
from detect.microsoft_api.microsoft_vision_api import analyze_image as ms_analyze, draw_resulted_images as ms_draw_results


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'results')
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_file_validity(request):
    if 'file' not in request.files:
        return False

    file = request.files['file']
    if file.filename == '':
        return False

    if not all([file, allowed_file(file.filename)]):
        return False

    return True


def save_file(request):
    file = request.files['file']
    secured_filename = str(datetime.datetime.now().timestamp()) + secure_filename(file.filename)
    image = Image.open(file)
    image.save(os.path.join(UPLOAD_FOLDER, secured_filename), quality=30, optimize=True)
    return secured_filename


def home_controller(request):
    is_file_valid = check_file_validity(request)
    if is_file_valid:
        secured_filename = save_file(request)
    else:
        return redirect(request.url)

    # Read language input / "trigger" button values
    translate_to = request.form.get('translate_to')
    type_button = request.form.get('type_analyse')
    handwrite_button = request.form.get('handwrite_analyse')
    custom_button = request.form.get('custom_analyse')

    # Set default detection method
    default_det_method = 'microsoft'
    default_hand_det_method = 'microsoft_advanced'
    default_options = option_dumps('0', translate_to)

    # React to each button accordingly
    if type_button:
        return redirect(url_for('app.analyse',
                                filename=secured_filename,
                                detection_method=default_det_method,
                                user_option=default_options))
    elif handwrite_button:
        return redirect(url_for('app.analyse',
                                filename=secured_filename,
                                detection_method=default_hand_det_method,
                                user_option=default_options))
    elif custom_button:
        return redirect(url_for('app.customize', filename=secured_filename))


def customize_options_controller(request, filename):
    detection_method_index = request.form.get('carousel_index')
    options_radio = request.form.get('options_radio')
    translate_to = request.form.get('translate_to')
    analyse_button = request.form.get('analyse_button')

    # If analyze button has been pressed
    if analyse_button:
        detection_method = possible_detection_methods.get(detection_method_index)
        option = option_dumps(options_radio, translate_to)
        return redirect(url_for('app.analyse', filename=filename, detection_method=detection_method, user_option=option))


def analyse_results_controller(filename, detection_method, user_option):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    user_option = json.loads(user_option)

    if os.path.isfile(file_path):
        # Detection and translation pipeline for Microsoft, Google APIs
        if detection_method in ['google', 'google_advanced', 'microsoft', 'microsoft_advanced']:
            return google_or_microsoft_analyse(filename, file_path, detection_method, user_option)
        elif detection_method in ['tesseract', 'abbyy']:
            return tesseract_or_abby_analyse(file_path, detection_method, user_option)
    else:
        return render_template('results.html', error='Image not uploaded!')


def google_or_microsoft_analyse(filename, file_path, detection_method, user_option):
    to_language = user_option.get('translate_to', None)
    advanced_mode = True if 'advanced' in detection_method else False

    if 'google' in detection_method:
        overall_text, words, words_and_boxes = g_analyze(file_path, advanced_mode)
    elif 'microsoft' in detection_method:
        overall_text, words, words_and_boxes = ms_analyze(file_path, advanced_mode)

    if all([overall_text, words, words_and_boxes]):
        translated_text, det_lang, translation_status = apply_options([overall_text], user_option)
        translated_words, det_lang, translation_status = apply_options(words, user_option)
        from_to_words_dict = {}

        if translation_status == 'success':
            from_to_words_dict = {words[i]: translated_words[i] for i in range(0, len(words))}
            translated_words_and_boxes = [[translated_words[i], word_box[1]] for i, word_box in enumerate(words_and_boxes)]
            if 'google' in detection_method:
                g_draw_results(translated_words_and_boxes, None, file_path, filename, 'translated')
            elif 'microsoft' in detection_method:
                ms_draw_results(translated_words_and_boxes, None, file_path, filename, 'translated', advanced_mode)   

        translated_text = translated_text.pop()
        overall_text = overall_text.replace('\n', '<br />')
        translated_text = translated_text.replace('\n', '<br />')

        return render_template(
            'results.html',
            detected_language=det_lang,
            to_language=to_language,
            original_text=overall_text,
            translated_text=translated_text,
            from_to_words=from_to_words_dict,
            original_filename=filename,
            partial_filename='granular_partial_' + filename,
            translated_filename='granular_translated_' + filename,
            translation_status=translation_status)
    else:
        return render_template('results.html', error='There was no text detected or the image was not accepted by the API!')


def tesseract_or_abby_analyse(file_path, detection_method, user_option):
    to_language = user_option.get('translate_to', None)

    if detection_method == 'tesseract':
        overall_text = pytesseract_to_string(file_path)
    elif detection_method == 'abbyy':
        overall_text = abbyy_to_string(file_path)

    if overall_text:
        translated_text, det_lang, translation_status = apply_options([overall_text], user_option)
        translated_text = translated_text.pop()
        overall_text = overall_text.replace('\n', '<br />')
        translated_text = translated_text.replace('\n', '<br />')

        return render_template(
            'results.html',
            detected_language=det_lang,
            to_language=to_language,
            original_text=overall_text,
            translated_text=translated_text,
            translation_status=translation_status)
    else:
        return render_template('results.html', error='There was no text detected or the image was not accepted by the API!')


def option_dumps(options_index, translate_to):
    selected_option = possible_lang_options.get(options_index)
    if selected_option.get('translate') == 'true':
        selected_option['translate_to'] = get_country_language(translate_to)
    return json.dumps(selected_option)


# How to download file
# return send_file(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), as_attachment=True)
