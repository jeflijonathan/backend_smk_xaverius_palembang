import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from common.utils.file_helper import validate_magic_number, cleanup_temp_file
from common.utils.file_location import generate_stored_filename, move_temp_to_location
from domains.uploadFile.upload_file_model import UploadFileModel


class UploadFileService:
    def __init__(self):
        self.temp_dir = "uploads/temp"
        self.permanent_dir = "uploads/files"
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.permanent_dir, exist_ok=True)

    async def upload_to_temp(self, file: UploadFile, db: Session) -> dict:
        stored_filename = generate_stored_filename(file.filename)
        temp_path = os.path.join(self.temp_dir, stored_filename)

        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            file_size = os.path.getsize(temp_path)
            if file_size > 5 * 1024 * 1024:
                cleanup_temp_file(temp_path)
                raise ValueError("File size exceeds 5MB limit")

 
            is_valid, mime_type = validate_magic_number(temp_path)
            if not is_valid:
                cleanup_temp_file(temp_path)
                raise ValueError(f"Invalid file type. Details: {mime_type}")

            file_url = temp_path.replace("\\", "/")

            file_record = UploadFileModel(
                original_name=file.filename,
                file_url=file_url,
                mime_type=mime_type,
                file_size=file_size,
            )
            db.add(file_record)
            db.commit()
            db.refresh(file_record)

            return {
                "id": file_record.id,
                "temp_filename": stored_filename,
                "original_name": file.filename,
                "file_url": file_url,
                "mime_type": mime_type,
                "file_size": file_size,
            }
        except ValueError:
            raise
        except Exception as e:
            cleanup_temp_file(temp_path)
            raise Exception("Internal Server Error") from e

    def get_file_by_id(self, db: Session, file_id: str):
        return db.query(UploadFileModel).filter(UploadFileModel.id == file_id).first()

    def get_all_files(self, db: Session, paginator: Optional[dict] = None):
        query = db.query(UploadFileModel)
        if paginator:
            search = paginator.get("value")
            if search and str(search).strip():
                kw = f"%{str(search).strip()}%"
                query = query.filter(UploadFileModel.original_name.ilike(kw))

            sort = paginator.get("sort")
            order_by = paginator.get("order_by", "desc")
            valid_sort_cols = {
                "original_name": UploadFileModel.original_name,
                "mime_type": UploadFileModel.mime_type,
                "file_size": UploadFileModel.file_size,
                "created_at": UploadFileModel.created_at,
            }
            sort_col = valid_sort_cols.get(sort, UploadFileModel.created_at)
            if order_by and str(order_by).lower() == "asc":
                query = query.order_by(sort_col.asc())
            else:
                query = query.order_by(sort_col.desc())

            page = int(paginator.get("page", 1))
            limit = paginator.get("limit")
            if limit is not None and int(limit) > 0:
                limit = int(limit)
                offset = (page - 1) * limit
                query = query.offset(offset).limit(limit)
        else:
            query = query.order_by(UploadFileModel.created_at.desc())

        return query.all()

    def count_all(self, db: Session, search: Optional[str] = None) -> int:
        query = db.query(UploadFileModel)
        if search and str(search).strip():
            kw = f"%{str(search).strip()}%"
            query = query.filter(UploadFileModel.original_name.ilike(kw))
        return query.count()

    def clear_temp_files(self, db: Session) -> dict:
        deleted_records = 0
        deleted_files = 0

        temp_records = db.query(UploadFileModel).filter(
            UploadFileModel.file_url.ilike("%uploads/temp%") |
            UploadFileModel.file_url.ilike("%uploads\\temp%") |
            UploadFileModel.file_url.ilike("%/temp/%") |
            UploadFileModel.file_url.ilike("%\\temp\\%")
        ).all()

        for record in temp_records:
            if record.file_url and os.path.exists(record.file_url):
                try:
                    os.remove(record.file_url)
                    deleted_files += 1
                except Exception:
                    pass
            db.delete(record)
            deleted_records += 1

        db.commit()

        if os.path.exists(self.temp_dir):
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        deleted_files += 1
                    except Exception:
                        pass

        return {
            "deleted_records": deleted_records,
            "deleted_files": deleted_files,
        }

    def delete_file(self, db: Session, file_id: str) -> bool:
        file_record = self.get_file_by_id(db, file_id)
        if not file_record:
            return False

        if file_record.file_url and os.path.exists(file_record.file_url):
            try:
                os.remove(file_record.file_url)
            except Exception:
                pass

        db.delete(file_record)
        db.commit()
        return True

    def bulk_delete_files(self, db: Session, file_ids: list[str]) -> dict:
        records = db.query(UploadFileModel).filter(UploadFileModel.id.in_(file_ids)).all()
        deleted_count = 0
        for record in records:
            if record.file_url and os.path.exists(record.file_url):
                try:
                    os.remove(record.file_url)
                except Exception:
                    pass
            db.delete(record)
            deleted_count += 1

        db.commit()
        return {"deleted_count": deleted_count}

