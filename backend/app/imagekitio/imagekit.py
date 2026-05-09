from imagekitio import AsyncImageKit

from app.core.config import settings
from app.core.logging import setup_logger

logger = setup_logger(__name__)

client = AsyncImageKit(
    private_key=settings.IMAGEKIT_API_KEY,
)


async def upload_file(file: bytes, file_name: str, **kwargs):
    try:
        res = await client.files.upload(
            file=file,
            file_name=file_name,
            folder=settings.IMAGEKIT_FILE_FOLDER,
            **kwargs,
        )

        return {
            "id": res.file_id,
            "url": res.url,
            "name": res.name,
            "type": res.file_type,
        }
    except Exception as error:
        logger.error(f"Failed to upload <{file_name}> to imagekit: {error}")
        raise Exception(error) from error


async def delete_file(file_id):
    return await client.files.delete(file_id)
