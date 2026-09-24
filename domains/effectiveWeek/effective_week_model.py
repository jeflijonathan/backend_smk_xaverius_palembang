import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, synonym
from config.database.db import Base
from common.consts.timestamps import Timestamps


def generate_uuid():
    return str(uuid.uuid4())


class EffectiveWeekModel(Base, Timestamps):
    __tablename__ = "effective_weeks"

    id_effective_week = Column(
        String(36), primary_key=True, default=generate_uuid, nullable=False
    )
    id = synonym("id_effective_week")

    id_subject = Column(
        String(36),
        ForeignKey("school_subjects.id_subject", ondelete="CASCADE"),
        nullable=False,
    )
    Alokasi_Intrakurikuler = Column(Integer, default=0, nullable=False)
    Alokasi_Kokurikuler = Column(Integer, default=0, nullable=False)

    subject = relationship(
        "SchoolSubjectModel", back_populates="effective_weeks"
    )
