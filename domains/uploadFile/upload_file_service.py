import os
import shutil
import uuid
from fastapi import UploadFile
from common.utils.file_helper import validate_magic_number, cleanup_temp_file
from common.utils.file_location import generate_stored_filename


class UploadFileService:
    def __init__(self):
        self.temp_dir = "uploads/temp"
        os.makedirs(self.temp_dir, exist_ok=True)

    async def upload_to_temp(self, file: UploadFile) -> dict:
        stored_filename = generate_stored_filename(file.filename)
        temp_path = os.path.join(self.temp_dir, stored_filename)

        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Validate size (5 MB limit)
            file_size = os.path.getsize(temp_path)
            if file_size > 5 * 1024 * 1024:
                cleanup_temp_file(temp_path)
                raise ValueError("File size exceeds 5MB limit")

            is_valid, mime_type = validate_magic_number(temp_path)
            if not is_valid:
                cleanup_temp_file(temp_path)
                raise ValueError(f"Invalid file type. Details: {mime_type}")

            return {
                "temp_filename": stored_filename,
                "original_name": file.filename,
                "mime_type": mime_type,
                "file_size": file_size,
            }
        except ValueError:
            raise
        except Exception as e:
            cleanup_temp_file(temp_path)
            raise Exception("Internal Server Error") from e
