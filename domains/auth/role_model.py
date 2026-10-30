import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from config.database.db import Base
from common.consts.timestamps import Timestamps
from domains.auth.associations import user_roles_association


def generate_uuid():
    return str(uuid.uuid4())


class RoleModel(Base, Timestamps):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True,
                default=generate_uuid, nullable=False)
    name = Column(String(50), unique=True, nullable=False, index=True)

    users = relationship(
        "UserModel", secondary=user_roles_association, back_populates="roles"
    )
