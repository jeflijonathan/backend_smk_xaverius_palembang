import os
from fastapi import Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.uploadFile.upload_file_service import UploadFileService


class UploadFileController(BaseController, prefix="/upload", tags=["Upload"]):
    def __init__(self):
        super().__init__()
        self.service = UploadFileService()
        self._register_routes()

    def _register_routes(self):

        @self.router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
        async def upload_file(file: UploadFile = File(...)):
            try:
                allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
                ext = os.path.splitext(file.filename)[1].lower()
                if ext not in allowed_extensions:
                    return self.handle_error(
                        detail=f"Extension {ext} not allowed. Allowed: {', '.join(allowed_extensions)}",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

                result = await self.service.upload_to_temp(file)

                return self.handle_success(
                    data=result,
                    message="File uploaded successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as ve:
                return self.handle_error(detail=str(ve), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return self.handle_error(detail="Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


upload_file_controller = UploadFileController()
router = upload_file_controller.get_router()
