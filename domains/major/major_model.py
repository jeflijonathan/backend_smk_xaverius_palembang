import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class MajorModel(Base, Timestamps):
    __tablename__ = "majors"

    id_major = Column(String(36), primary_key=True, default=generate_uuid, nullable=False)
    id = synonym("id_major")

    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    classes = relationship(
        "ClassModel",
        back_populates="major",
        cascade="all, delete-orphan"
    )
    subjects = relationship(
        "SchoolSubjectModel",
        back_populates="major"
    )
