from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.auth.role_model import RoleModel


class RoleController(BaseController, prefix="/roles", tags=["Roles"]):

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_roles(db: Session = Depends(get_db)):
            try:
                roles = db.query(RoleModel).filter(RoleModel.deleted_at == None).all()
                data = [{"id": r.id, "name": r.name} for r in roles]
                return cls.handle_success(data=data, message="Roles retrieved successfully")
            except Exception as error:
                cls.handle_error(detail=str(error))


RoleController.register_routes()
router = RoleController.get_router()
