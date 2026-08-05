import os
import uuid

from fastapi import APIRouter, File, HTTPException,UploadFile
from config import ALLOWED_EXTENSIONS,MAX_FILE_SIZE_MB,UPLOAD_DIR
from service.document_parser import extract_text
from models import Contract



router=APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)


@router.post("/upload")
async def upload_contract():
    """Upload a PDF or TXT contract for analysis"""
    file=UploadFile=File(...)
    ext=os.path.splittext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=404,detail="File type not allowed")
    content=await file.read()
    size_mb=len(content)/(1024*1024)
    if size_mb>MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400,detail="file size exeeds maximum limit i.e 10")
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    unique_name=f"{uuid.uuid4().hex}{ext}"
    file_path=os.path.join(UPLOAD_DIR,unique_name)
    with open(file_path,"wb") as f:
        f.write(content)
    parsed=extract_text(file_path)
    return {"message":"contracts uploaded successfully"}