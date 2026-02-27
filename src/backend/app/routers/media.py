from typing import Any
import io
import uuid
import aioboto3
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from PIL import Image

from app.config import settings
from app.engine import get_db
from app.dependencies import get_current_user
from app.models import PatientChecklist, PatientStatus
from app.schemas import PatientChecklistResponse

media_router = APIRouter(prefix="/media", tags=["Media"])

async def upload_to_s3(file_data: bytes, file_name: str, content_type: str):
    session = aioboto3.Session()
    s3_context: Any = session.client(
        's3',
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name="us-east-1"
    )
    
    async with s3_context as s3:
        await s3.put_object(
            Bucket=settings.s3_bucket,
            Key=file_name,
            Body=file_data,
            ContentType=content_type
        )
    
    return f"{settings.s3_endpoint}/{settings.s3_bucket}/{file_name}"


@media_router.post("/upload/{checklist_item_id}", response_model=PatientChecklistResponse)
async def upload_document(
    checklist_item_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image allowed")

    result = await db.execute(
        select(PatientChecklist).where(PatientChecklist.id == checklist_item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist record not found")

    content = await file.read()
    image = Image.open(io.BytesIO(content))
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
    buffer = io.BytesIO()
    image.save(buffer, "WEBP", quality=70, optimize=True)
    buffer.seek(0)

    file_name = f"{uuid.uuid4()}.webp"
    s3_url = await upload_to_s3(buffer.getvalue(), file_name, "image/webp")

    item.file_path = s3_url
    item.status = PatientStatus.LOADED
    
    await db.commit()
    await db.refresh(item, ["task"])

    return PatientChecklistResponse(
        id=item.id,
        task_id=item.task_id,
        task_title=item.task.title,
        status=item.status,
        value=item.value,
        file_path=item.file_path
    )
