import uuid

import aioboto3
from fastapi import HTTPException, UploadFile

from src.config import settings

aws_access_key_id = settings.AWS_ACCESS_KEY_ID
aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
s3_bucket = settings.AWS_S3_BUCKET_NAME
region_name = settings.AWS_REGION_NAME
allowed_extensions = {"png", "jpg", "jpeg"}


def allowed_file(filename: str) -> bool:
    is_allowed = (
        "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )
    return is_allowed


async def upload_file_to_s3(file: UploadFile) -> str:
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    unique_filename = f"uploads/{uuid.uuid4().hex}_{file.filename}"
    session = aioboto3.Session()
    async with session.client(
        "s3",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    ) as s3_client:
        try:
            await s3_client.upload_fileobj(file.file, s3_bucket, unique_filename)
            file_url = (
                f"https://{s3_bucket}.s3.{region_name}.amazonaws.com/{unique_filename}"
            )
            return file_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {e}")
