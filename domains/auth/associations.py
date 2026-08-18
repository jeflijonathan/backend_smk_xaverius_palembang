from sqlalchemy import Table, Column, String, ForeignKey
from config.database.db import Base

student_roles_association = Table(
    "student_roles_users",
    Base.metadata,
    Column(
        "student_id",
        String(36),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

employee_roles_association = Table(
    "employee_roles_users",
    Base.metadata,
    Column(
        "employee_id",
        String(36),
        # Diubah ke 'employees.id' (jamak)
        ForeignKey("employees.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


user_roles_association = Table(
    "user_roles_association",
    Base.metadata,
    Column(
        "user_id",
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

