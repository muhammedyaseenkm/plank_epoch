from flask import Blueprint, request, jsonify, current_app
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

upload_file_blueprint = Blueprint('file_uploader', __name__)

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'}

class FileUploader:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=5)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_uploaded_file(self, uploaded_file, upload_folder):
        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)
        return file_path

    def check_file_existence(self, upload_folder, filename):
        return os.path.exists(os.path.join(upload_folder, filename))

    async def process_file(self, uploaded_file, upload_folder):
        if not self.allowed_file(uploaded_file.filename):
            return {'error': 'File type not allowed'}, 400

        filename = uploaded_file.filename
        file_path = self.save_uploaded_file(uploaded_file, upload_folder)
        return {'message': f'{filename} File uploaded successfully', 'file_path': file_path}, 200

    def upload_file_async(self, uploaded_file, upload_folder):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self.process_file(uploaded_file, upload_folder))
        loop.run_until_complete(future)
        return future.result()

    def upload_file_threaded(self, uploaded_file, upload_folder):
        return self.executor.submit(self.process_file, uploaded_file, upload_folder)

@upload_file_blueprint.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        filename = uploaded_file.filename

        # Check if file already exists
        if FileUploader().check_file_existence(upload_folder, filename):
            return jsonify({'error': 'File already exists'}), 400

        # Execute file upload asynchronously
        file_uploader = FileUploader()
        result = file_uploader.upload_file_async(uploaded_file, upload_folder)
        return jsonify(result), 200

    elif request.method == 'GET':
        return jsonify({'message': 'Upload endpoint. POST a file.'}), 200
