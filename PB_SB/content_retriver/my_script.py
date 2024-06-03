from unstructured.partition.pdf import partition_pdf
import os

def extract_pdf_element(path, file_name, output_path):
    # Call partition_pdf to extract elements from the PDF file
    partition_pdf(
        filename=os.path.join(path, file_name),
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy='by_title',
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        extract_image_block_output_dir=output_path
    )

def iterate_through_output_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)            
            print("Processing file:", file_path)            
            extract_pdf_element(directory, filename, output_path)

# Define the output directory path
output_path = r'D:\PB_SB\content_retriver\PatientSatisfactioninClinicalHealthcareDataAnalytics'

iterate_through_output_files(output_path)
