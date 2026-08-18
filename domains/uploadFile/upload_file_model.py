from sqlalchemy import func, Column, Integer, String, DateTime
from config.database.db import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class UploadFileModel(Base):
    __tablename__ = "upload_files"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    original_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
