from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import jwt
from config.database.db import get_db
from config.env.env import env


def get_current_user_payload(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1].strip()
    elif request.cookies.get("access_token"):
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autentikasi diperlukan. Token akses tidak ditemukan.",
        )

    try:
        payload = jwt.decode(token, env.jwtSecret, algorithms=[env.jwtAlgorithm])
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token bukan access token yang valid.",
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token telah kedaluwarsa. Silakan refresh token.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tanda tangan token tidak valid.",
        )


def require_roles(allowed_roles: List[str]):
    def role_checker(payload: dict = Depends(get_current_user_payload)):
        user_roles = [str(r).lower() for r in payload.get("roles", [])]
        active_role = payload.get("active_role")
        allowed_lower = [str(r).lower() for r in allowed_roles]

        # Check either active_role or any user roles matching
        has_role = False
        if active_role and str(active_role).lower() in allowed_lower:
            has_role = True
        elif any(r in allowed_lower for r in user_roles):
            has_role = True

        if not has_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak. Fitur ini hanya diperuntukkan bagi role: {', '.join(allowed_roles)}.",
            )
        return payload

    return role_checker

