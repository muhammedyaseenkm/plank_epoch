import PyPDF2
import os
import zipfile

# Path to the ZIP file containing the PDF
zip_file_path = r'C:\Users\Planck Epoch\Desktop\AI image\Child-Health-Record-Form.zip'

# Output folder to extract the ZIP contents
output_folder = r'C:\Users\Planck Epoch\Desktop\AI image\Child-Health-Record-Form'

# Extract the PDF file from the ZIP


"""
def extract_pdf(file_name):
    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    pdf_file.close()  # Close the file after use
    return num_pages
"""

def extract_pdf(file_name):
    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    # Iterate through each page and extract text
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        print(f"Page {page_num + 1}:\n{page_text}\n")
    pdf_file.close()  # Close the file after use
    return num_pages

def unzip(zip_file_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)

unzip(zip_file_path, output_folder)

# Get the PDF file path
pdf_file_name = ''
pdf_file_path = os.path.join(output_folder, pdf_file_name)
pdf_file_path = r'C:\Users\Planck Epoch\Desktop\AI image\Child-Health-Record-Form'
pdf_file_path = r'Child Health Record Form.pdf'


# Get the number of pages in the PDF
num_pages = extract_pdf(pdf_file_path)
print("Number of pages in the PDF:", num_pages)
