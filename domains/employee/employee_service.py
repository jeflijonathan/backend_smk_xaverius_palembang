from typing import Any
from typing_extensions import Dict
from typing_extensions import Optional
from typing import List
from sqlalchemy.orm import Session
from domains.employee.employee_repository import EmployeeRepository
from domains.employee.dto.employee_schema import EmployeeCreate, EmployeeUpdate
from domains.uploadFile.upload_file_model import UploadFileModel
import os
import shutil


class EmployeeService:
    def __init__(self):
        self.repo = EmployeeRepository()

    def get_all(self, db: Session, paginator: Optional[Dict[str, Any]] = None) -> List:
        search = paginator.get("value") if paginator else None
        sort = paginator.get("sort") if paginator else None
        order_by = paginator.get("order_by") if paginator else None
        return self.repo.find_all(db, paginator=paginator, search=search, sort=sort, order_by=order_by)
    
    def get_by_id(self, db: Session, id: str):
        return self.repo.find_by_id(db, id)

    def count_all(self, db: Session, search: Optional[str] = None) -> int:
        return self.repo.count_all(db, search=search)

    def _process_profile_image(self, db: Session, file_id: str):
        file_record = db.query(UploadFileModel).filter(UploadFileModel.id == file_id).first()
        if not file_record:
            raise ValueError("Profile image file not found")
        
        valid_mimes = ["image/jpeg", "image/jpg", "image/png"]
        if file_record.mime_type not in valid_mimes:
            raise ValueError("Uploaded file is not a valid image (jpg/jpeg/png).")
            
        if "uploads/temp" in file_record.file_url or "uploads\\temp" in file_record.file_url:
            dest_dir = "uploads/employee"
            os.makedirs(dest_dir, exist_ok=True)
            filename = os.path.basename(file_record.file_url)
            dest_path = os.path.join(dest_dir, filename)
            
            try:
                shutil.move(file_record.file_url, dest_path)
                file_record.file_url = dest_path.replace("\\", "/")
                db.commit()
            except FileNotFoundError:
                pass

    def _delete_profile_image(self, db: Session, file_id: str):
        file_record = db.query(UploadFileModel).filter(UploadFileModel.id == file_id).first()
        if file_record:
            if os.path.exists(file_record.file_url):
                try:
                    os.remove(file_record.file_url)
                except Exception:
                    pass
            db.delete(file_record)
            db.commit()

    def create_employee(self, db: Session, data: EmployeeCreate):
        if data.profile.profile_url:
            self._process_profile_image(db, data.profile.profile_url)
            
        user_data = data.user.model_dump()
        detail_data = data.detail.model_dump(exclude_unset=True) if data.detail else None
        role_ids = data.role_ids or []
        return self.repo.create_employee(db, user_data, data.profile.model_dump(), detail_data, role_ids)

    def update_employee(self, db: Session, id: str, data: EmployeeUpdate):
        old_employee = self.repo.find_by_id(db, id)
        if not old_employee:
            return None
        old_profile_url_id = old_employee.profile_url if old_employee else None

        if data.profile_url and data.profile_url != old_profile_url_id:
            self._process_profile_image(db, data.profile_url)
            if old_profile_url_id:
                self._delete_profile_image(db, old_profile_url_id)

        update_dict = data.model_dump(exclude={'detail', 'username', 'password', 'role_ids'}, exclude_unset=True)
        user_data = {}
        if data.username is not None and data.username.strip():
            user_data["username"] = data.username.strip()
        if data.password is not None and data.password.strip():
            user_data["password"] = data.password.strip()
        
        detail_data = data.detail.model_dump(exclude_unset=True) if data.detail else None
        role_ids = data.role_ids
        return self.repo.update_employee(db, id, user_data or None, update_dict or None, detail_data, role_ids)

    def delete_employee(self, db: Session, id: str):
        return self.repo.delete_employee(db, id)
