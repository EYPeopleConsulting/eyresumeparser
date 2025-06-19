import os
import re
import fitz  # PyMuPDF for PDF
from docx import Document

def extract_text_from_pdf(filepath, max_pages=3):
    try:
        doc = fitz.open(filepath)
        if doc.page_count == 0:
            print(f"⚠️ PDF has 0 pages: {filepath}")
            return "ERROR_PARSING_FILE"

        pages_to_read = min(doc.page_count, max_pages)
        text = "\n".join([doc.load_page(i).get_text() for i in range(pages_to_read)])

        if not text.strip():
            print(f"⚠️ No extractable text in: {filepath}")
            return "ERROR_PARSING_FILE"

        return text

    except Exception as e:
        print(f"❌ Error reading PDF: {filepath} - {e}")
        return "ERROR_PARSING_FILE"

def extract_text_from_docx(filepath):
    try:
        doc = Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text.strip():
            print(f"⚠️ No text found in DOCX: {filepath}")
            return "ERROR_PARSING_FILE"
        return text
    except Exception as e:
        print(f"❌ Error reading DOCX: {filepath} - {e}")
        return "ERROR_PARSING_FILE"

def extract_text_from_file(filepath):
    ext = filepath.lower()
    if ext.endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif ext.endswith('.docx'):
        return extract_text_from_docx(filepath)
    else:
        print(f"⚠️ Unsupported file format: {filepath}")
        return "ERROR_PARSING_FILE"

def extract_contact_info(text):
    email = re.search(r'\S+@\S+', text)
    phone = re.search(r'\+?\d[\d \-\(\)]{8,15}\d', text)
    name = text.strip().split('\n')[0][:50]
    return name.strip(), email.group() if email else '', phone.group() if phone else ''

def extract_resumes(folder_path):
    resumes = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.pdf', '.docx')):
            full_path = os.path.join(folder_path, file)
            text = extract_text_from_file(full_path)
            if "ERROR_PARSING_FILE" in text or not text.strip():
                print(f"⚠️ Skipping unreadable resume: {file}")
                continue
            name, email, phone = extract_contact_info(text)
            resumes.append({
                'filename': file,
                'text': text,
                'name': name or file.replace('.pdf', '').replace('.docx', ''),
                'email': email,
                'phone': phone
            })
    return resumes

def extract_jd_text(request):
    jd_file = request.files.get('jd_file')
    jd_text = request.form.get('jd_text', '').strip()

    if jd_file and jd_file.filename:
        path = os.path.join('uploads', jd_file.filename)
        os.makedirs('uploads', exist_ok=True)
        jd_file.save(path)
        jd_text = extract_text_from_file(path)

    return jd_text.strip()
