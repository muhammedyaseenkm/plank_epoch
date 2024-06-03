import subprocess
import shutil
import os 
from urllib.parse import urlparse, unquote
from unstructured.partition.pdf import partition_pdf

def open_pdf_file(file_path):
    try:
        folder_name = 'pdf_downloads'
        subprocess.Popen(['start', file_path], shell=True)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)
        parsed_url = urlparse(file_path)
        file_name = os.path.basename(parsed_url.path)
        decoded_file_path = unquote(parsed_url.path)  # Decode percent-encoded characters
        # Remove the leading slash from the path
        if decoded_file_path.startswith("/"):
            decoded_file_path = decoded_file_path[1:]
        shutil.copyfile(decoded_file_path, os.path.join(folder_name, file_name))

    except subprocess.CalledProcessError:
        print("Error: Unable to open the PDF file.")
    except FileNotFoundError:
        print("Error: 'xdg-open' command not found. This command is typically available on Linux systems.")

# Provide the path to your PDF file
pdf_file_path = "file:///C:/Users/Planck%20Epoch/Desktop/nihms-987752.pdf"

# Open the PDF file
open_pdf_file(pdf_file_path)
elements = partition_pdf(pdf_file_path)


