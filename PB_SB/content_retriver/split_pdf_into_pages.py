from PyPDF2 import PdfReader, PdfWriter
import os

# Path to the raw PDF file
raw_pdf_file = r'D:\PB_SB\content_retriver\raw_pdf_folder\PatientSatisfactioninClinicalHealthcareDataAnalytics.pdf'

base_name = os.path.basename(raw_pdf_file)
output_folder = os.path.splitext(base_name)[0] 
os.makedirs(output_folder, exist_ok=True)

input_pdf = PdfReader(raw_pdf_file)

for i, page in enumerate(input_pdf.pages):
    output_pdf = PdfWriter()
    output_pdf.add_page(page)
    output_file_path = os.path.join(output_folder, f'{output_folder}_page_{i+1}.pdf')
    with open(output_file_path, 'wb') as output_file:
        output_pdf.write(output_file)
        print(f'Page {i+1} saved to {output_file_path}')
