# app.py

def execute():
    python_commands = [
        'from unstructured.partition.pdf import partition_pdf',
        'elements = partition_pdf(filename="example-docs/layout-parser-paper-fast.pdf")',
        'from unstructured.partition.text import partition_text',
        'elements = partition_text(filename="example-docs/fake-text.txt")'
        'print(elements)'
    ]
    return python_commands
