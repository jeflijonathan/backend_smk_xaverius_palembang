import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database.db import engine, Base

# Import all models to ensure they are registered with the Base metadata
import domains.auth.role_model
import domains.student.student_model
import domains.employee.employee_model
import domains.users.user_model
import domains.uploadFile.upload_file_model
import domains.categorySubject.category_subject_model
import domains.major.major_model
import domains.subject.subject_model
import domains.effectiveWeek.effective_week_model
import domains.teacherSubject.teacher_subject_model
import domains.schoolInformation.school_information_model
import domains.classes.class_model
import domains.classroom.classroom_model
import domains.schedule.schedule_model

if __name__ == "__main__":
    print("Creating all tables in database...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")
