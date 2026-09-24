from domains.student.student_controller import StudentController
from domains.student.student_model import StudentModel
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.env.env import env
from domains.users.user_controller import UserController
from domains.uploadFile.upload_file_controller import UploadFileController
from config.limiter.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import asyncio
import os
import time


async def cleanup_temp_files_periodic(interval_seconds: int = 10, max_age_seconds: int = 10):
    temp_dir = "uploads/temp"
    while True:
        await asyncio.sleep(interval_seconds)
        if not os.path.exists(temp_dir):
            continue
        current_time = time.time()
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age_seconds:
                    try:
                        os.remove(file_path)
                        print(f"[Cleanup] Cleaned up old temp file: {file_path}")
                    except Exception as e:
                        print(f"[Cleanup Error] Failed to remove temp file {file_path}: {e}")


class Router:
    def __init__(self):
        self.app = FastAPI(title="Python API Server", version="1.0")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.state.limiter = limiter
        self.app.add_exception_handler(
            RateLimitExceeded, _rate_limit_exceeded_handler)

        from fastapi.exceptions import HTTPException
        from fastapi.responses import JSONResponse

        @self.app.exception_handler(HTTPException)
        async def http_exception_handler(request, exc):
            if isinstance(exc.detail, dict):
                return JSONResponse(
                    status_code=exc.status_code,
                    content=exc.detail
                )
            return JSONResponse(
                status_code=exc.status_code,
                content={"status": "error", "status_code": exc.status_code, "message": exc.detail}
            )
        self.host = env.beHost
        self.port = int(env.bePort)
        self._setup_routes()

    def _setup_routes(self):
        # self.app.include_router(UserController.get_router(), prefix="/api")
        self.app.include_router(StudentController.get_router(), prefix="/api")
        self.app.include_router(UploadFileController.get_router(), prefix="/api")

        from domains.employee.employee_controller import EmployeeController
        self.app.include_router(EmployeeController.get_router(), prefix="/api")

        from domains.subject.subject_controller import SubjectController
        self.app.include_router(SubjectController.get_router(), prefix="/api")

        from domains.categorySubject.category_subject_controller import CategorySubjectController
        self.app.include_router(CategorySubjectController.get_router(), prefix="/api")

        from domains.major.major_controller import MajorController
        self.app.include_router(MajorController.get_router(), prefix="/api")

        from domains.schoolInformation.school_information_controller import SchoolInformationController
        self.app.include_router(SchoolInformationController.get_router(), prefix="/api")

        from domains.classes.class_controller import ClassController
        self.app.include_router(ClassController.get_router(), prefix="/api")

        from domains.teacherSubject.teacher_subject_controller import TeacherSubjectController
        self.app.include_router(TeacherSubjectController.get_router(), prefix="/api")

        from domains.classroom.classroom_controller import ClassroomController
        self.app.include_router(ClassroomController.get_router(), prefix="/api")

        from domains.schedule.schedule_controller import (
            CategoryScheduleTimeController,
            ScheduleTimeController,
            ScheduleController,
        )
        self.app.include_router(CategoryScheduleTimeController.get_router(), prefix="/api")
        self.app.include_router(ScheduleTimeController.get_router(), prefix="/api")
        self.app.include_router(ScheduleController.get_router(), prefix="/api")

        from domains.effectiveWeek.effective_week_controller import EffectiveWeekController
        self.app.include_router(EffectiveWeekController.get_router(), prefix="/api")

        @self.app.get("/")
        def root():
            return {"message": "Welcome to Python FastAPI + MySQL!"}

        @self.app.get("/api/health-check")
        def health_check():
            return {"status": "OK", "message": "Health check passed"}

        @self.app.on_event("startup")
        async def startup_event():
            asyncio.create_task(cleanup_temp_files_periodic(
                interval_seconds=10, max_age_seconds=10))

    def listen(self):
        print(f"[Server] Server running at http://{self.host}:{self.port}")

        uvicorn.run(
            "main:router_instance.app",
            host=self.host,
            port=self.port,
            reload=True,
            timeout_graceful_shutdown=3,
        )
