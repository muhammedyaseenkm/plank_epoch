import os
import tabula
import json
import pandas as pd
from unstructured.partition.csv import partition_csv
#from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.docx import partition_xlsx
from unstructured.partition.image import partition_image

def categorize(file_name):
    file_extension = os.path.splitext(file_name)[1].lower()
    
    if file_extension == '.pdf':
        elements = partition_pdf(file_name)
        return elements
    elif file_extension == '.csv':
        elements = partition_csv(file_name)
        return elements
    elif file_extension == '.docx':
        elements = partition_docx(file_name)
        return elements
    elif file_extension == '.xlsx':
        elements = partition_xlsx(file_name)
        return elements
    elif file_extension in ['.jpg', '.png', '.gif']:
        elements = partition_image(file_name)
        return elements
    else:
        # Handle unsupported file types
        print(f"Unsupported file type: {file_extension}")
        return None

# Example usage:
file_name = "Child Health Record Form.pdf"
elements = categorize(file_name)
print(elements)
