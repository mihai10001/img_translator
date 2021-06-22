import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
# Detection pipeline wrappers
from detect.detection_methods import possible_detection_methods
from detect.abbyy_api.abbyy_vision_api import abbyy_to_string
from detect.tesseract_sdk.pytess_detect import pytesseract_to_string
from detect.google_ocr_api.google_vision_api import analyze_image as g_analyze, draw_resulted_images as g_draw_results
from detect.microsoft_ocr_api.microsoft_computer_vision import analyze_image as ms_analyze, draw_resulted_images as ms_draw_results
# Translation pipeline wrapper
from language.language_options import apply_options, possible_lang_options, get_country_language
# from cleanup import remove_static_files_win
# call remove_static_files() to clean 

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'results')
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def add_header(r):
    """
    Disable caching as for now, it happens server-side.
    """
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET', 'POST'])
def home():

    # POST: Triggered when the user presses a HTML button.
    if request.method == 'POST':
        # Read language input / "trigger" button values:
        # If the input is empty or the buttons have not been pressed
        # their values will be None ( null ).
        translate_to = request.form.get('translate_to')
        type_button = request.form.get('type_analyse')
        handwrite_button = request.form.get('handwrite_analyse')
        custom_button = request.form.get('custom_analyse')
        # Set default detection method
        default_det_method = 'google'
        default_hand_det_method = 'google_advanced'
        default_options = option_dumps('0', translate_to)

        # Check if indeed a button has been pressed to continue,
        # by checking if the values are different from None ( null ).
        if any([type_button, handwrite_button, custom_button]):

            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)

            if file and allowed_file(file.filename):
                secured_filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, secured_filename))

                # React to each button accordingly
                if type_button:
                    return redirect(url_for('analyse',
                                            filename=secured_filename,
                                            detection_method=default_det_method,
                                            user_option=default_options))
                if handwrite_button:
                    return redirect(url_for('analyse',
                                            filename=secured_filename,
                                            detection_method=default_hand_det_method,
                                            user_option=default_options))
                if custom_button:
                    return redirect(url_for('customize', filename=secured_filename))

    return render_template('home.html')


@app.route('/customize/<filename>', methods=['GET', 'POST'])
def customize(filename):

    if filename:
        if request.method == 'POST':
            detection_method_index = request.form.get('carousel_index')
            options_radio = request.form.get('options_radio')
            translate_to = request.form.get('translate_to')
            analyse_button = request.form.get('analyse_button')

            # if download_button:
            #     return send_file(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), as_attachment=True)
            if analyse_button:
                detection_method = possible_detection_methods.get(detection_method_index)
                option = option_dumps(options_radio, translate_to)
                return redirect(url_for('analyse', filename=filename, detection_method=detection_method, user_option=option))

        return render_template('customize.html', filename=filename)
    else:
        return render_template('customize.html', error='Image not uploaded!')


@app.route('/analyse/<filename>/<detection_method>/<user_option>', methods=['GET', 'POST'])
def analyse(filename, detection_method, user_option):
    user_option = json.loads(user_option)
    to_language = user_option.get('translate_to')
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.isfile(image_path):
        # Detection and translation pipeline for Microsoft, Google APIs
        if detection_method in ['google', 'google_advanced', 'microsoft', 'microsoft_advanced']:
            advanced_mode = True if 'advanced' in detection_method else False
            if 'google' in detection_method:
                overall_text, words, words_and_boxes = g_analyze(image_path, advanced_mode)
            elif 'microsoft' in detection_method:
                overall_text, words, words_and_boxes = ms_analyze(image_path, advanced_mode)

            if all([overall_text, words, words_and_boxes]):
                translated_text = apply_options([overall_text], user_option)[0].pop()
                translated_words, det_lang = apply_options(words, user_option)
                from_to_words_dict = {words[i]: translated_words[i] for i in range(0, len(words))}
                translated_words_and_boxes = [[translated_words[i], word_box[1]] for i, word_box in enumerate(words_and_boxes)]
                if 'google' in detection_method:
                    g_draw_results(translated_words_and_boxes, None, image_path, filename, 'translated')
                elif 'microsoft' in detection_method:
                    ms_draw_results(translated_words_and_boxes, None, image_path, filename, 'translated', advanced_mode)

                overall_text = overall_text.replace('\n', '<br />')
                translated_text = translated_text.replace('\n', '<br />')

                return render_template('results.html',
                                       detected_language=det_lang,
                                       to_language=to_language,
                                       original_text=overall_text,
                                       translated_text=translated_text,
                                       from_to_words=from_to_words_dict,
                                       original_filename=filename,
                                       partial_filename='granular_partial_' + filename,
                                       translated_filename='granular_translated_' + filename)

            else:
                return render_template('results.html', error='There was no text detected or the image was not accepted by the API!')

        elif detection_method in ['tesseract', 'abbyy']:
            if detection_method == 'tesseract':
                overall_text = pytesseract_to_string(image_path)
            elif detection_method == 'abbyy':
                overall_text = abbyy_to_string(image_path)
            if overall_text:
                translated_text, det_lang = apply_options([overall_text], user_option)
                translated_text = translated_text.pop()
                overall_text = overall_text.replace('\n', '<br />')
                translated_text = translated_text.replace('\n', '<br />')
                return render_template('results.html',
                                       detected_language=det_lang,
                                       to_language=to_language,
                                       original_text=overall_text,
                                       translated_text=translated_text)
            else:
                return render_template('results.html', error='There was no text detected or the image was not accepted by the API!')

    else:
        return render_template('results.html', error='Image not uploaded!')


def option_dumps(options_index, translate_to):
    selected_option = possible_lang_options.get(options_index)
    selected_option['translate_to'] = get_country_language(translate_to)
    return json.dumps(selected_option)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT'))
    app.run(debug=True)
