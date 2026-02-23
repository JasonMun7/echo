from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.auth import get_current_uid
from app.services.gcs import upload_file

router = APIRouter(prefix="/storage", tags=["storage"])


@router.post("/upload")
async def upload(
    file: UploadFile,
    uid: str = Depends(get_current_uid),
):
    try:
        content = await file.read()
        blob_name = f"users/{uid}/{file.filename or 'file'}"
        path = upload_file(blob_name, content, file.content_type)
        return {"path": path}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
