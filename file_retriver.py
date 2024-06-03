from flask import Blueprint, request, jsonify, current_app, send_file
import os
import openpyxl


file_retrive_blueprint = Blueprint('file_retriver', __name__)

UPLOAD_FOLDER = os.getcwd()

@file_retrive_blueprint.route('/file_list')
def file_list():
    dir_path =  current_app.config.get('UPLOAD_FOLDER')
    file_name = [file for file in os.listdir(dir_path)]
    return jsonify(file_name)

@file_retrive_blueprint.route('/file_content/<filename>')
def file_content(filename):
    dir_path = current_app.config.get('UPLOAD_FOLDER')
    file_path = os.path.join(dir_path, filename)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        if filename.endswith('.xlsx'):
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            data = []
            for row in  sheet.iter_rows(values_only=True):
                data.append(row)
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': f'{filename} is not an Excel file'}), 400
    else:
        return jsonify({'error': 'File not found'}), 404
     