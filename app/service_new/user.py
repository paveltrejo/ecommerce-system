from sqlalchemy.orm import Session
from repository.user import UserRepository
from schema.user.user import UserCreate, UserModify
from model.user.user import User, UserRole
from typing import List

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def get_all_users(self, is_active: bool) -> List[User]:
        return self.user_repo.get_all_users(is_active)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repo.get_user_by_id(user_id)
    
    def get_user_by_email(self, user_email:str) -> User:
        return self.user_repo.get_user_by_email(user_email)

    def create_user(self, new_user: UserCreate, user_role: UserRole) -> User:
        return self.user_repo.create_user(new_user, user_role)

    def update_user(self, user_id: int, modify_user: UserModify) -> int:
        return self.user_repo.update_user(user_id, modify_user)

    def delete_user(self, user_id: int) -> dict:
        return self.user_repo.delete_user(user_id)