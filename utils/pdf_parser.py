from io import BytesIO
from pypdf import PdfReader

def extract_pdf_text(file_bytes):
    pdf = PdfReader(BytesIO(file_bytes))

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text