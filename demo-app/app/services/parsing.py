from pathlib import Path
from pypdf import PdfReader


def parse_text_file(file_path: Path) -> str:
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def parse_pdf_file(file_path: Path) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def parse_file(file_path: Path, content_type: str) -> str:
    if content_type == "application/pdf" or file_path.suffix.lower() == ".pdf":
        return parse_pdf_file(file_path)
    return parse_text_file(file_path)