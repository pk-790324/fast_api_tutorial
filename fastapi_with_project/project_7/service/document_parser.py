

import os

from PyPDF2 import PdfReader


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    return text.strip()


def extract_text(file_path: str) -> str:
    """
    Extract text from a document file.

    Args:
        file_path (str): Path to the document file.

    Returns:
        str: Extracted text.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")