import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class SchoolSubjectModel(Base, Timestamps):
    __tablename__ = "school_subjects"

    id = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    name = Column(String(255), nullable=False)
    category_subject_id = Column(String(36), ForeignKey("category_subjects.id", ondelete="CASCADE"), nullable=False)

    category = relationship("CategorySubjectModel", back_populates="subjects")
