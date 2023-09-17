# Stdlib Imports
import os
import secrets
from pathlib import Path

# FastAPI Imports
from fastapi.responses import JSONResponse
from fastapi import APIRouter, BackgroundTasks, File, UploadFile, HTTPException

# Own Imports
from apps.commoners.services.cloudinary_upload import file_uploader
from apps.commoners.utils import (
    remove_file_from_root_directory,
    RecursionDepth,
)

# Third Party Imports
import aiofiles
from asyncer import asyncify


# initialize api router
router = APIRouter(tags=["Commoners"], prefix="/commoners")

# Set value of bytes
BYTES_SIZE: int = 1000000



@router.post("/upload/")
async def upload_image(
    tasks: BackgroundTasks, file_in_memory: UploadFile = File(...)
) -> JSONResponse:
    """API Router for uploading image.

    Returns:
        JSONResponse: _description_
    """

    # get parent directory
    parent_directory = Path(__file__).absolute().parent.parent
    image_directory = "/static/images/"

    # generate a secret token hex
    secret_filename = secrets.token_hex(8) + ".png"

    # join parent and secret_filename to generate wav audio path
    file_path = os.path.join(f"{parent_directory}{image_directory}", secret_filename)

    # Read the file contents
    file_contents = await file_in_memory.read()
    if len(file_contents) / BYTES_SIZE >= 4:
        raise HTTPException(400, {"message": "File size must not exceed 4MB"})

    # override the recursion depth level to avoid infinite recursion
    with RecursionDepth(3000):
        # upload image to disk
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(file_contents)

    # upload audio to cloudinary
    upload_url = await asyncify(file_uploader.upload_file)(file_path)

    # remove uploaded files from the parent directory
    tasks.add_task(remove_file_from_root_directory, f"{parent_directory}{image_directory}")

    return JSONResponse(
        {
            "message": "File upload successfully",
            "data": {"upload_url": upload_url},
        }
    )
