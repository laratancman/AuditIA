from fastapi import APIRouter, UploadFile, File
from app.utils import extract_text_from_docx, extract_text_from_pdf
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_path)
    elif file.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        return {"error": "Formato não suportado"}

    return {
        "filename": file.filename,
        "content": extracted_text[:1000]  # Exibe só os primeiros 1000 caracteres
    }
