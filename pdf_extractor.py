import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """يستخرج النص من ملف PDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text
