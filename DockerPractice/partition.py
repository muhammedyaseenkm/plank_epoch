from  script import execute_pdf, execute_text, execute_api, execute_image, ExitStack

# Call the execute function if script.py is executed directly
file_name_to_save_elements  = 'extracted_elements'


if __name__ == "__main__":
    # Example usage:
    pdf_filename = "D:\\DockerPractice\\pdf_downloads\\nihms-987752.pdf"
    execute_pdf(pdf_filename, "pdf_elements.txt")
    execute_text("example-docs/fake-text.txt", "text_elements.txt")
    execute_image("example-docs/layout-parser-paper-fast.jpg", "image_elements.txt", languages=["eng", "swe"])

    filenames = ["example-docs/fake-email.eml", "example-docs/fake.docx"]
    execute_api(filenames, output_file="api_elements.txt")