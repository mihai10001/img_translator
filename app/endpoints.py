import os
from flask import Flask, render_template, request
from controllers import home_controller, customize_options_controller, analyse_results_controller
# from cleanup import remove_static_files_win
# call remove_static_files() to clean 


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'results')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.after_request
def add_header(r):
    """
    Disable caching
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
        return home_controller(request)
    elif request.method == 'GET':
        return render_template('home.html')



@app.route('/customize/<filename>', methods=['GET', 'POST'])
def customize(filename):
    if filename:
        if request.method == 'POST':
            return customize_options_controller(request, filename)
        elif request.method == 'GET':
            return render_template('customize.html', filename=filename)
    else:
        return render_template('customize.html', error='Image not uploaded!')



@app.route('/analyse/<filename>/<detection_method>/<user_option>', methods=['GET', 'POST'])
def analyse(filename, detection_method, user_option):
    if filename:
        return analyse_results_controller(filename, detection_method, user_option)
    else:
        return render_template('results.html', error='Image not uploaded!')



if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT'))
    app.run(debug=True)
