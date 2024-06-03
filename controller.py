import requests

# Function to upload file to Server B
def upload_file_to_server_b(file_path):
    url = "http://localhost:8000/upload/"  # Server B's upload endpoint
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    return response.json()