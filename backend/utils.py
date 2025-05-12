import os
import docx
import PyPDF2

def load_file_text(file_path, file_name):
    ext = os.path.splitext(file_name)[1].lower()
    
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def load_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def load_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])
