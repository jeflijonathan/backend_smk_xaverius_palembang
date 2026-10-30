from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Query, status
import math


class PaginationParams:
    """Dependency class untuk query params pagination, search, dan sort."""
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Nomor halaman (mulai dari 1)"),
        limit: int = Query(default=10, ge=1, le=100, description="Jumlah data per halaman (max 100)"),
        value: Optional[str] = Query(default=None, description="Kata kunci pencarian"),
        sort: Optional[str] = Query(default=None, description="Kolom untuk sorting"),
        order_by: Optional[str] = Query(default="desc", description="Arah sorting: asc atau desc"),
    ):
        self.page = page
        self.limit = limit
        self.value = value
        self.sort = sort
        self.order_by = order_by

    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "limit": self.limit,
            "value": self.value,
            "sort": self.sort,
            "order_by": self.order_by,
        }


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
        message: str = "SUCCESS",
        status_code: int = status.HTTP_200_OK,
    ) -> dict:
        return {
            "status": "SUCCESS",
            "status_code": status_code,
            "message": message,
            "data": data if data is not None else {},
        }

    @staticmethod
    def handle_paginated_success(
        data: Any,
        total_data: int,
        page: int,
        limit: int,
        message: str = "SUCCESS",
        status_code: int = status.HTTP_200_OK,
    ) -> dict:
        total_pages = math.ceil(total_data / limit) if limit > 0 else 1
        return {
            "status": "SUCCESS",
            "status_code": status_code,
            "message": message,
            "data": {
                "data": data if data is not None else [],
                "pagination": {
                    "total_data": total_data,
                    "page": page,
                    "limit": limit,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1,
                },
            },
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

