import fitz      # PyMuPDF's Python module is imported as fitz.


def extract_text_from_pdf(file_path:str):
    ## Extract all the text from a pdf and return it in a single string

    document =fitz.open(file_path)
    extracted_text =""
    for page in document:
        extracted_text +=page.get_text()

    document.close()
    return extracted_text    