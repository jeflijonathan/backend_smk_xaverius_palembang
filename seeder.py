"""
Seeder script untuk:
1. Membuat semua roles
2. Membuat akun employee pertama (admin)

Jalankan di dalam container:
    docker exec -it presensi-app python seeder.py
"""
import os
import sys
import uuid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database.db import SessionLocal, engine, Base

# Import semua model
import domains.auth.role_model
import domains.student.student_model
import domains.employee.employee_model
import domains.users.user_model
import domains.uploadFile.upload_file_model
import domains.announcement.announcement_model

from domains.auth.role_model import RoleModel
from domains.users.user_model import UserModel
from domains.employee.employee_model import EmployeeModel, EmployeeDetailModel


def generate_uuid():
    return str(uuid.uuid4())


# ═══════════════════════════════════════════════════════════════
# Daftar Roles
# ═══════════════════════════════════════════════════════════════
ROLES = [
    "guru",
    "kepala_sekolah",
    "wali_kelas",
    "bidang_keuangan",
    "guru_piket",
    "kurikulum",
    "pembimbing_pkl",
    "kesiswaan",
    "admin",
    "staff",
    "siswa",
    "pengurus_kelas",
]


def seed_roles(db):
    """Seed roles ke database (skip jika sudah ada)."""
    print("\n[Seeder] Seeding roles...")
    created = 0
    for role_name in ROLES:
        existing = db.query(RoleModel).filter(RoleModel.name == role_name).first()
        if not existing:
            role = RoleModel(id=generate_uuid(), name=role_name)
            db.add(role)
            created += 1
            print(f"  ✔ Created role: {role_name}")
        else:
            print(f"  - Skipped (exists): {role_name}")
    db.commit()
    print(f"[Seeder] Roles done. Created: {created}, Total: {len(ROLES)}")


def seed_first_employee(db):
    """Seed akun employee pertama dengan role admin + guru."""
    print("\n[Seeder] Seeding first employee...")

    # Cek apakah user admin sudah ada
    existing_user = db.query(UserModel).filter(UserModel.username == "admin").first()
    if existing_user:
        print("  - Skipped (user 'admin' already exists)")
        return

    # 1. Buat User
    user = UserModel(
        id=generate_uuid(),
        full_name="Administrator",
        username="admin",
        password="admin123",
        status=True,
    )
    db.add(user)
    db.flush()

    # 2. Assign roles: admin
    admin_role = db.query(RoleModel).filter(RoleModel.name == "admin").first()
    if admin_role:
        user.roles = [admin_role]
        db.flush()
        print(f"  ✔ Assigned role: admin")

    # 3. Buat Employee profile
    employee = EmployeeModel(
        id=generate_uuid(),
        user_id=user.id,
        first_name="Admin",
        last_name="Xaverius",
        niy="ADM001",
        email="admin@smkxaverius.sch.id",
        status=True,
    )
    db.add(employee)
    db.flush()

    # 4. Buat Employee detail
    detail = EmployeeDetailModel(
        id=generate_uuid(),
        employee_id=employee.id,
        gender="L",
        birth_place="Palembang",
        address="SMK Xaverius Palembang",
        phone_number="08123456789",
        description="Admin Sekolah",
    )
    db.add(detail)

    db.commit()
    print(f"  ✔ Created employee: Admin Xaverius (username: admin, password: admin123)")


def run_seeder():
    print("=" * 60)
    print("  SMK Xaverius Palembang - Database Seeder")
    print("=" * 60)

    # Buat semua tabel yang belum ada
    Base.metadata.create_all(bind=engine)
    print("[Seeder] Tables ensured.")

    db = SessionLocal()
    try:
        seed_roles(db)
        seed_first_employee(db)
        print("\n" + "=" * 60)
        print("  Seeder completed successfully! ✔")
        print("=" * 60)
    except Exception as e:
        db.rollback()
        print(f"\n[Seeder] ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seeder()
