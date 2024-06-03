import PyPDF2
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from unstructured.partition.pdf import partition_pdf

def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def parse_pdf(pdf_path):
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    parsed_text = ""
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        parsed_text += parse_layout(layout)

    return parsed_text

def parse_layout(layout):
    parsed_text = ""
    for obj in layout._objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            parsed_text += obj.get_text().replace('\n', '_')
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parsed_text += parse_layout(obj._objs)
    return parsed_text

def doc_partition(pdf_path):
    raw_pdf_elements = partition_pdf(
        filename=pdf_path,
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=pdf_path)
    return raw_pdf_elements

# Example usage
pdf_path = r"D:\DOCUMENT_EXTRACTION\Child Health Record Form.pdf"
parsed_text = extract_text(pdf_path)
print(parsed_text)

parsed_layout = parse_pdf(pdf_path)
print(parsed_layout)

raw_pdf_elements = doc_partition(pdf_path)
