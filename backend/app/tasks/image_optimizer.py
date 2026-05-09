import io

import httpx
from PIL import Image
from imagekitio import ImageKitError

from app.core.logging import setup_logger
from app.imagekitio.imagekit import upload_file
from app.tasks.registry import task
from app.worker_logic.exception import TaskException

logger = setup_logger(__name__)


@task("image_optimize")
async def image_optimize(payload: list[dict]):
    if not payload:
        raise ValueError("Payload is missing")

    result = []
    for image_metadata in payload:
        image_type = image_metadata.get("type", None)
        image_name = image_metadata.get("name", None)
        image_format = image_metadata.get("format", None)
        image_url = image_metadata.get("url", None)

        if not image_type or not image_name or not image_format or not image_url:
            raise ValueError("Invalid payload structure")

        allowed_formats = ["JPG", "JPEG", "PNG", "GIF", "WEBP", "AVIF"]
        if image_type != "image":
            raise ValueError("Invalid image file")
        if str(image_format).upper() not in allowed_formats:
            raise ValueError(f"Invalid image format. (Allowed:{allowed_formats})")

        res_image = httpx.get(image_url)
        res_image.raise_for_status()

        input_buffer = io.BytesIO(res_image.content)
        output_buffer = io.BytesIO()

        image = Image.open(input_buffer)
        image.thumbnail((800, 800))
        image.save(output_buffer, format="WEBP", optimize=True, quality=85)

        try:
            res = await upload_file(
                file=output_buffer.getvalue(),
                file_name=image_name,
                overwrite_file=True,
                use_unique_file_name=False,
            )
            result.append(res)
        except ImageKitError as error:
            logger.error(f"Failed to upload image <{image_name}> to imagekit : {error}")
            raise TaskException(error) from error

    return result
