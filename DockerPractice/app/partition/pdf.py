import subprocess
from PyPDF2 import PdfReader


def execute_pdf(filename, output_file):
    try:
        # Define the command for PDF partitioning
        command = f"docker exec -it unstructured python3 -c \"from unstructured.partition.pdf import partition_pdf; partition_pdf(filename='{filename}', strategy='hi_res', extract_images_in_pdf=True, extract_image_block_types=['Image', 'Table'], extract_image_block_to_payload=False, extract_image_block_output_dir='path/to/save/images')\""

        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("PDF partitioning executed successfully.")
        else:
            print(f"PDF partitioning failed with return code: {result.returncode}")

        with open(output_file, "w") as f:
            f.write(result.stdout)

    except subprocess.CalledProcessError as e:
        print("PDF partitioning failed:", e)
    except Exception as e:
        print("An error occurred during PDF partitioning:", e)


def partition_pdf(filename):
    elements = []  # Initialize an empty list to store extracted text elements
    try:
        with open(filename, 'rb') as file:
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text = page.extract_text()
                # Depending on your requirements, you might want to further process the text
                elements.append(text)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return elements

# Example usage:
pdf_filename = "D:\\DockerPractice\\pdf_downloads\\nihms-987752.pdf"
extracted_elements = partition_pdf(pdf_filename)
# print(extracted_elements)
execute_pdf(pdf_filename, "pdf_elements.txt")
