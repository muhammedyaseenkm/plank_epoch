from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_random_image():
    # Replace this with your actual image generation logic
    # For demonstration purposes, generating a random RGB image
    width, height = 200, 200
    image_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return image_array

@app.route('/api/upload-images', methods=['POST'])
def upload_images():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    uploaded_files = request.files.getlist('files')
    image_names = []
    for file in uploaded_files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_names.append(filename)
    return jsonify({'uploaded_images': image_names})

def search_image(image_name):
    found_images = []
    for root, _, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if image_name.lower() in file.lower():
                found_images.append(os.path.join(root, file))
    return found_images

@app.route('/api/first-image')
def get_first_image():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return jsonify({'message': 'No images uploaded yet'}), 404

    first_image_path = os.path.join(app.config['UPLOAD_FOLDER'], files[0])
    found_images = search_image(files[0])
    if found_images:
        first_found_image = found_images[0]
        return send_file(first_found_image, mimetype='image/jpeg')
    else:
        return jsonify({'message': f'No images found with name: {files[0]}'}), 404
    
@app.route('/api/image/<filename>')
def get_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
    #    return jsonify({'message': f'Image {filename} not found'}), 404
        return send_file('random_image.png', 'image/png')

    

@app.route('/get-image', methods=['GET'])
def get_random_image():
    image_array = generate_random_image()
    img = Image.fromarray(image_array)
    img.save('random_image.png')
    return send_file('random_image.png', 'image/png')

if __name__ == '__main__':
    app.run(debug=True)
