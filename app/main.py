import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from detect.pytess_detect import load_image
from language.language_options import apply_options
from cleanup import remove_static_files

UPLOAD_FOLDER = os.getcwd() + '/static'
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    remove_static_files()

    if request.method == 'POST':
        submit_button = request.form.get('submit_button')

        if submit_button == 'upload_image':
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect(request.url)

            if file and allowed_file(file.filename):
                secured_filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, secured_filename))
                return redirect(url_for('uploaded', filename=secured_filename))

    return render_template('home.html')


@app.route('/uploaded/<filename>', methods=['GET', 'POST'])
def uploaded(filename):

    if filename:
        if request.method == 'POST':
            analyse_button = request.form.get('analyse_button')
            # if download_button:
            #     return send_file(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), as_attachment=True)
            if analyse_button:
                options = json.dumps({'translate': '1', 'translate_to': 'en'})
                return redirect(url_for('analysed', filename=filename, user_options=options))

        return render_template('uploaded.html', filename=filename)
    else:
        return render_template('uploaded.html', error='Image not uploaded!')


@app.route('/analysed/<filename>/<user_options>', methods=['GET', 'POST'])
def analysed(filename, user_options):
    user_options = json.loads(user_options)

    if filename:
        image = load_image(os.path.join(UPLOAD_FOLDER, filename))
        random_strings = ["Buna sera, doamna", "Oare ce facem aici", "Unde e aici ?"]
        random_text = apply_options(random_strings, user_options)

        if request.method == 'POST':
            print('wow')

        return render_template('analysed.html', filename=filename, random_text=random_text, image=image)
    else:
        return render_template('analysed.html', error='Image not uploaded!')



if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT'))
    app.run(debug=True)
