import asyncio
import aioboto3
from src.backend.app.config import settings

from typing import Any

async def upload_to_s3(file_data: bytes, file_name: str, content_type: str):
    session = aioboto3.Session()

    s3_client: Any = session.client(
        's3',
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name="us-east-1"
    )
    
    async with s3_client as s3:
        await s3.put_object(
            Bucket=settings.s3_bucket,
            Key=file_name,
            Body=file_data,
            ContentType=content_type
        )
    
    return f"{settings.s3_endpoint}/{settings.s3_bucket}/{file_name}"


if __name__ == "__main__":
    asyncio.run(test_connection())
