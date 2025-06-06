import os
from PyPDF2 import PdfReader

def pdf_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def list_documents(doc_dir):
    return [os.path.join(doc_dir, f) for f in os.listdir(doc_dir) if f.endswith(('.pdf', '.txt'))]