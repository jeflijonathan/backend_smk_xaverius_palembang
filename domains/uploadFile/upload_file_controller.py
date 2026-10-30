import os
from fastapi import Depends, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController, PaginationParams
from domains.uploadFile.upload_file_service import UploadFileService
from domains.uploadFile.dto.upload_file_schema import UploadFileResponseDTO, UploadFileResponse, BulkDeleteDTO

class UploadFileController(BaseController, prefix="/upload", tags=["Upload"]):
    def __init__(self):
        super().__init__()
        self.service = UploadFileService()
        self._register_routes()

    def _register_routes(self):

        @self.router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
        async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
            try:
                allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf", ".docx", ".doc", ".xls", ".xlsx", ".pptx", ".ppt", ".zip", ".rar"}
                ext = os.path.splitext(file.filename)[1].lower()
                if ext not in allowed_extensions:
                    return self.handle_error(
                        detail=f"Extension {ext} not allowed. Allowed: {', '.join(allowed_extensions)}",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

                result = await self.service.upload_to_temp(file, db)

                return self.handle_success(
                    data=result,
                    message="File uploaded successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as ve:
                return self.handle_error(detail=str(ve), status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return self.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        @self.router.get("/", status_code=status.HTTP_200_OK)
        def get_all_files(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
            try:
                paginator_dict = pagination.to_dict()
                files = self.service.get_all_files(db, paginator=paginator_dict)
                total_data = self.service.count_all(
                    db,
                    search=paginator_dict.get('value'),
                )
                data = [UploadFileResponseDTO.model_validate(f).model_dump() for f in files]

                return self.handle_paginated_success(
                    data=data,
                    total_data=total_data,
                    page=pagination.page,
                    limit=pagination.limit,
                    message="Files retrieved successfully",
                    status_code=status.HTTP_200_OK,
                )
            except Exception as error:
                return self.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        @self.router.delete("/temp", status_code=status.HTTP_200_OK)
        @self.router.delete("/temp/", status_code=status.HTTP_200_OK)
        def clear_temp_files(db: Session = Depends(get_db)):
            try:
                result = self.service.clear_temp_files(db)
                return self.handle_success(
                    data=result,
                    message="Temporary files cleared successfully",
                    status_code=status.HTTP_200_OK,
                )
            except Exception as error:
                return self.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3. Get Data Metadata by ID (GET - Mengambil detail metadata file dalam bentuk JSON)
        # Dibedakan rutenya dengan endpoint download file fisik
        @self.router.get("/meta/{file_id}", status_code=status.HTTP_200_OK)
        def get_file_metadata(file_id: str, db: Session = Depends(get_db)):
            try:
                file_record = self.service.get_file_by_id(db, file_id)
                if not file_record:
                    return self.handle_error(
                        detail="File not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                data = UploadFileResponseDTO.model_validate(file_record).model_dump()
                return self.handle_success(
                    data=data,
                    message="File metadata retrieved successfully",
                    status_code=status.HTTP_200_OK,
                )
            except Exception as error:
                return self.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. Download / Stream File by ID (GET - Mengunduh file aslinya)
        @self.router.get("/{file_id}", status_code=status.HTTP_200_OK)
        def get_file(file_id: str, db: Session = Depends(get_db)):
            try:
                file_record = self.service.get_file_by_id(db, file_id)
                if not file_record:
                    return self.handle_error(
                        detail="File not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

                file_path = file_record.file_url
                if not os.path.isabs(file_path) and not os.path.exists(file_path):
                    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
                    alt_path = os.path.normpath(os.path.join(backend_dir, file_path))
                    if os.path.exists(alt_path):
                        file_path = alt_path

                if not os.path.exists(file_path):
                    return self.handle_error(
                        detail="File not found on disk",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

                return FileResponse(
                    path=file_path,
                    media_type=file_record.mime_type,
                    filename=file_record.original_name,
                )
            except Exception as e:
                import traceback
                traceback.print_exc()
                if hasattr(e, 'status_code'):
                    raise e
                return self.handle_error(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5. Bulk Delete Files (POST - Menghapus banyak file sekaligus berdasarkan array id)
        @self.router.post("/bulk-delete", status_code=status.HTTP_200_OK)
        def bulk_delete_files(payload: BulkDeleteDTO, db: Session = Depends(get_db)):
            try:
                result = self.service.bulk_delete_files(db, payload.ids)
                return self.handle_success(
                    data=result,
                    message=f"{result['deleted_count']} files deleted successfully",
                    status_code=status.HTTP_200_OK,
                )
            except Exception as error:
                return self.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 6. Delete File by ID (DELETE - Menghapus file tunggal)
        @self.router.delete("/{file_id}", status_code=status.HTTP_200_OK)
        def delete_file(file_id: str, db: Session = Depends(get_db)):
            try:
                success = self.service.delete_file(db, file_id)
                if not success:
                    return self.handle_error(
                        detail="File not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return self.handle_success(
                    data={"id": file_id},
                    message="File deleted successfully",
                    status_code=status.HTTP_200_OK,
                )
            except Exception as error:
                return self.handle_error(detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


upload_file_controller = UploadFileController()
router = upload_file_controller.get_router()