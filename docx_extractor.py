from docx import Document

def extract_text_from_docx(docx_path: str) -> str:
    """يستخرج النص من ملف DOCX."""
    text = ""
    try:
        document = Document(docx_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    return text
