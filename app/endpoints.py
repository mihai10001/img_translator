from flask import Blueprint, render_template, request
import os
from flask import Flask, render_template, request
from controllers import home_controller, customize_options_controller, analyse_results_controller


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
            return render_template('customize.html', filename=filename)
    else:
        return render_template('customize.html', error='Image not uploaded!')


@app_endpoints.route('/analyse/<filename>/<detection_method>/<user_option>', methods=['GET', 'POST'])
def analyse(filename, detection_method, user_option):
    if filename:
        return analyse_results_controller(filename, detection_method, user_option)
    else:
        return render_template('results.html', error='Image not uploaded!')
