# index.py
from handlers.file_uploader import upload_file_blueprint
from handlers.file_retriver import file_retrive_blueprint

from flask import Flask
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')


app.register_blueprint(upload_file_blueprint)
app.register_blueprint(file_retrive_blueprint)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
