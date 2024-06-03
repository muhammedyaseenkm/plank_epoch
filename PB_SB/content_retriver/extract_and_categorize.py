from unstructured.partition.pdf import partition_pdf
from unstructured import unstructured_inference
import os


raw_pdf_file = r'D:\PB_SB\content_retriver\raw_pdf_folder\PatientSatisfactioninClinicalHealthcareDataAnalytics.pdf'

base_name = os.path.basename(raw_pdf_file)
output_folder = os.path.splitext(base_name)[0] 
os.makedirs(output_folder, exist_ok=True)


def extract_pdf_element(path, file_name, output_path):
    return partition_pdf(
        filename=os.path.join(path, file_name),
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy='by_title',
        max_character = 5000,                                  # 17377,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        extract_image_block_output_dir=output_path
    )