import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class CategorySubjectModel(Base, Timestamps):
    __tablename__ = "category_subjects"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    status = Column(Boolean, default=True, nullable=False)

    subjects = relationship(
        "SchoolSubjectModel",
        back_populates="category",
        cascade="all, delete-orphan"
    )
