from fastapi import APIRouter, UploadFile

from src.aws.utils import upload_file_to_s3

router = APIRouter(tags=["upload"], prefix="/upload")


@router.post("/")
async def create_upload_file(file: UploadFile):
    url = await upload_file_to_s3(file=file)
    return {"url": url}
