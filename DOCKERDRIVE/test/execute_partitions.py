from unstructured.partition.pdf import partition_pdf
from unstructured.partition.text import partition_text

# Partition PDF file
pdf_elements = partition_pdf(filename="example-docs/layout-parser-paper-fast.pdf")

# Partition text file
text_elements = partition_text(filename="example-docs/fake-text.txt")

# Print results
print("PDF Elements:")
print(pdf_elements)

print("Text Elements:")
print(text_elements)
