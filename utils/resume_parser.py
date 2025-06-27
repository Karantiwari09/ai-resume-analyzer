import fitz

def extract_text_from_pdf(file):
    """
    Extracts text from uploaded PDF file using PyMuPDF.
    :param file: Uploaded file from Streamlit uploader
    :return: Extracted text as a single string
    """
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.lower()
