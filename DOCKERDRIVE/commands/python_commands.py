def execute():
    from unstructured.partition.pdf import partition_pdf
    elements_pdf = partition_pdf(filename="example-docs/layout-parser-paper-fast.pdf")
    
    from unstructured.partition.text import partition_text
    elements_text = partition_text(filename="example-docs/fake-text.txt")

    return elements_pdf, elements_text

execute()
