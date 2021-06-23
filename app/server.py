import os
from flask import Flask
from endpoints import app_endpoints

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'results')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


if __name__ == "__main__":
    app.register_blueprint(app_endpoints)
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT'))
