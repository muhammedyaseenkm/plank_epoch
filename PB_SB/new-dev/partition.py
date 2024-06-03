"""
from unstructured.partition.auto import partition
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import open_filename

# Rest of the code...
# ...
# ...

elements = partition(filename="example-docs/eml/fake-email.eml")
print(elements)
"""


import PyPDF2

def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Example usage
pdf_path = "/content/drive/MyDrive/Patient Assesment Report Form.pdf"
pdf_path = r"Child Health Record Form.pdf"
text = extract_text(pdf_path)
print(text)
