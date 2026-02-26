from pathlib import Path


def extract_text_from_file(file_path: str) -> str:
    """
    Placeholder extractor.
    Replace with robust PDF/DOCX/OCR pipeline in production.
    """
    suffix = Path(file_path).suffix.lower()
    if suffix in [".pdf", ".docx", ".jpg", ".jpeg", ".png"]:
        return f"Extracted placeholder text from {Path(file_path).name}."
    return ""
