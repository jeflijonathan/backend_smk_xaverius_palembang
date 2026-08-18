from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config.env.env import env

# 1. Susun URL Koneksi
DATABASE_URL = f"{env.dbConnection}://{env.dbUser}:{env.dbPassword}@{env.dbHost}:{env.dbPort}/{env.dbName}"

# 2. Buat Engine Database
engine = create_engine(DATABASE_URL, echo=env.dbLogging)

# 3. Buat Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4. Standar SQLAlchemy 2.0 untuk membuat Base Class Model
class Base(DeclarativeBase):
    pass


# 5. Helper Dependency Injection untuk FastAPI Controller
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import all models to register them with SQLAlchemy Base.metadata
import domains.auth.role_model
import domains.student.student_model
import domains.employee.employee_model
import domains.users.user_model
import domains.uploadFile.upload_file_model
import domains.categorySubject.category_subject_model
import domains.subject.subject_model

