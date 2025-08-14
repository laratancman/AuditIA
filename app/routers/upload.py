import os.path

from fastapi import UploadFile, File, HTTPException
from app.ia.vectorstore import init_vectorstore, ingest_documents
from app.ia.utils import upload_file, chunk_split, read_pdf
from fastapi import APIRouter
import uuid

router = APIRouter(prefix="/documents", tags=["Chat"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Arquivo deve ser PDF")
    temp_path = f"/tmp/{uuid.uuid4()}.pdf"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    s3_key = f"documents/{os.path.basename(temp_path)}"
    s3_url = upload_file(temp_path, s3_key)
    pdf_text = read_pdf(file_path=temp_path)
    chunks = chunk_split(pdf_text)

    metadatas = [{"source": s3_url, "chunk": i} for i in range(len(chunks))]
    ingest_documents(chunks, metadatas, init_vectorstore())    


