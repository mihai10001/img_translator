from flask import Blueprint, render_template, request, Response
from detect.detection_methods import detection_methods_full_description
from controllers import home_controller, customize_options_controller, analyse_results_controller
from cleanup import remove_static_files

app_endpoints = Blueprint('app', __name__)


@app_endpoints.route('/', methods=['GET', 'POST'])
def home():
    # POST: Triggered when the user presses a HTML button.
    if request.method == 'POST':
        return home_controller(request)
    elif request.method == 'GET':
        return render_template('home.html')


@app_endpoints.route('/customize/<filename>', methods=['GET', 'POST'])
def customize(filename):
    if filename:
        if request.method == 'POST':
            return customize_options_controller(request, filename)
        elif request.method == 'GET':
            return render_template('customize.html', filename=filename,
                                   detection_methods_description=detection_methods_full_description)
    else:
        return render_template('customize.html', error='Image not uploaded!')


@app_endpoints.route('/analyse/<filename>/<detection_method>/<user_option>', methods=['GET', 'POST'])
def analyse(filename, detection_method, user_option):
    if filename:
        return analyse_results_controller(filename, detection_method, user_option)
    else:
        return render_template('results.html', error='Image not uploaded!')


# Used to remove stored images periodically, as Heroku tends to complain about file sizes
@app_endpoints.route('/cleanup')
def cleanup_static_files():
    remove_static_files()
    return Response(status=201)
