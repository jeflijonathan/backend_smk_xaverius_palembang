from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.users.user_model import UserModel


class UserRepository(BaseMySQLService[UserModel]):
    def __init__(self):
        super().__init__(UserModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[UserModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id: str) -> Optional[UserModel]:
        return self.find_one(db, {"id": id})

    def create_user(self, db: Session, data: Dict[str, Any]) -> UserModel:
        return self.create(db, data)

    def update_user(
        self, db: Session, id: str, data: Dict[str, Any]
    ) -> Optional[UserModel]:
        return self.update(db, id, data)

    def delete_user(self, db: Session, id: str) -> Optional[UserModel]:
        return self.delete(db, {"id": id})
