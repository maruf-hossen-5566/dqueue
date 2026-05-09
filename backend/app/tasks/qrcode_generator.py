import io
import uuid

import qrcode
from imagekitio import ImageKitError

from app.core.logging import setup_logger
from app.imagekitio.imagekit import upload_file
from app.tasks.registry import task
from app.worker_logic.exception import TaskException

logger = setup_logger(__name__)


@task("qrcode_generate")
async def qrcode_generate(payload: str):
    if not payload or not payload.strip():
        raise ValueError("Payload is missing")

    try:
        image = qrcode.make(payload)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")

        res = await upload_file(
            file=buffer.getvalue(),
            file_name=f"{str(uuid.uuid4()).replace('-', '_')}.png",
        )
        return [res]
    except ImageKitError as error:
        logger.error(f"Failed to upload QR code image to imagekit: {error}")
        raise TaskException(error) from error
    except Exception as error:
        logger.error(f"Failed to generate QR code: {error}")
        raise TaskException(error) from error
