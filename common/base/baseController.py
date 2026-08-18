from typing import Any, Optional
from fastapi import APIRouter, HTTPException, status


class BaseController:
    router: APIRouter

    def __init_subclass__(cls, prefix: str = "", tags: Optional[list] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.router = APIRouter(prefix=prefix, tags=tags or [])

    @classmethod
    def get_router(cls) -> APIRouter:
        return cls.router

    @staticmethod
    def handle_success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> dict:
        return {
            "status": "success",
            "status_code": status_code,
            "message": message,
            "data": data if data is not None else {},
        }

    @staticmethod
    def handle_error(
        detail: str = "Internal Server Error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Any] = None,
    ):
        error_payload = {
            "status": "error",
            "status_code": status_code,
            "message": detail,
        }
        if details is not None:
            error_payload["details"] = details

        raise HTTPException(status_code=status_code, detail=error_payload)
