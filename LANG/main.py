from typing import Any
import os
from unstructured.partition.pdf import partition_pdf
#import pytesseract 
from pathlib import Path


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

file_path = '/content/drive/MyDrive/Patient Assesment Report Form.pdf'
file_name = os.path.basename(file_path)
input_path = os.path.join(file_path[:-(len(file_name))], )
print(input_path, file_name)


output_path = os.path.join(os.getcwd(), file_name)
print(output_path)


# Specify the file path
file_path = Path("/content/drive/MyDrive/Patient Assesment Report Form.pdf")
image_path ="/content/page_image.png"


raw_elements = partition_pdf(
    file_name="",
    extract_image_in_pdf =True,
    infer_table_structure=True,
    chunkings_strategy="by_title",
    max_characters=4000,
    new_after_n_chars=3800,
    combine_text_under_n_chars=2000,
    image_output_dir_path=output_path
)
