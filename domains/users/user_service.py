from typing import List, Optional
from sqlalchemy.orm import Session
from domains.users.user_model import UserModel
from domains.users.user_repository import UserRepository
from domains.users.dto.user_dto import CreateUserDTO, UpdateUserDTO


class UserService:
    def __init__(self):
        self._user_repository = UserRepository()

    def get_all_users(self, db: Session) -> List[UserModel]:
        return self._user_repository.find_all(db)

    def create_user(self, db: Session, user_data: CreateUserDTO) -> UserModel:
        email_exists = self._user_repository.find_one(db, {"email": user_data.email})
        if email_exists:
            raise ValueError("Email already registered!")

        data_dict = user_data.model_dump()
        return self._user_repository.create_user(db, data_dict)

    def update_user(
        self, db: Session, user_id: int, update_data: UpdateUserDTO
    ) -> Optional[UserModel]:
        clean_update_data = update_data.model_dump(exclude_unset=True)

        if not clean_update_data:
            return self._user_repository.find_one(db, {"id": user_id})

        if "email" in clean_update_data:
            email_exists = self._user_repository.find_one(
                db, {"email": clean_update_data["email"]}
            )

            if email_exists and email_exists.id != user_id:
                raise ValueError("Email already in use by another user!")

        user = self._user_repository.update_user(db, user_id, clean_update_data)

        if not user:
            raise ValueError("User not found!")

        return user
