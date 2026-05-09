import io
import uuid

import httpx
from imagekitio import ImageKitError
from pypdf import PdfWriter

from app.core.logging import setup_logger
from app.imagekitio.imagekit import delete_file, upload_file
from app.tasks.registry import task
from app.worker_logic.exception import TaskException

logger = setup_logger(__name__)


@task("merge_pdf")
async def merge_pdf(payload: list[dict]):
    if not payload:
        raise ValueError("Payload is missing")

    pdfs_to_merge = []

    for file_metadata in payload:
        file_id = file_metadata.get("id", None)
        file_name = file_metadata.get("name", None)
        file_format = file_metadata.get("format", None)
        file_url = file_metadata.get("url", None)

        if not file_id or not file_format or not file_format or not file_url:
            raise ValueError("Invalid payload structure")

        if str(file_format).lower() != "pdf":
            raise ValueError(f"Invalid file format '{file_name}'. (Allowed: PDF)")

        stored_file = httpx.get(file_url)
        stored_file.raise_for_status()
        pdfs_to_merge.append(io.BytesIO(stored_file.content))

        try:
            await delete_file(file_id=file_id)
        except ImageKitError as error:
            logger.error(f"Failed to delete file <{file_id}> from imagekit: {error}")
            continue

    merger = PdfWriter()
    for pdf in pdfs_to_merge:
        merger.append(pdf)

    pdf_buffer = io.BytesIO()
    merger.write(pdf_buffer)

    try:
        res = await upload_file(
            file=pdf_buffer.getvalue(),
            file_name=f"merged_{str(uuid.uuid4()).replace('-', '_')}.pdf",
        )
        return [res]
    except ImageKitError as error:
        logger.error(f"Failed to upload PDF to imagekit: {error}")
        raise TaskException(error) from error
