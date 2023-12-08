from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model.user.user import User, UserRole
from schema.user.user import UserCreate, UserModify
from typing import List
from utils.hash import hash_str

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self, is_active: bool) -> List[User]:
        return self.db.query(User).filter_by(is_active=is_active).all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter_by(id=user_id).first()
    
    def get_user_by_email(self, user_email: str) -> User:
        return self.db.query(User).filter_by(email=user_email).first()

    def create_user(self, new_user: UserCreate, user_role: UserRole) -> User:
        db_user = None
        try:
            db_user = User(
                email = new_user.email, 
                hashed_pass=hash_str(new_user.hashed_pass),  
                is_active = new_user.is_active,
                created_at =new_user.created_at,
                role=user_role
                )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except SQLAlchemyError as e:
            print("#=================")
            print(e)
            print("#=================")
            db_user = None
            return db_user
        except Exception as ex:
            print(f"No se pudo guardar en la base de datos: {ex}")
        return db_user

    def update_user(self, user_id: int, modify_user: UserModify) -> int:
        rows_updated = (
            self.db.query(User)
            .filter_by(id=user_id)
            .update(modify_user, synchronize_session="fetch")
        )
        self.db.commit()
        return rows_updated

    def delete_user(self, user_id: int) -> dict:
        user = self.db.query(User).filter(User.id == user_id).first()
        self.db.delete(user)
        self.db.commit()
        return user