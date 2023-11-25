from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from utils.hash import hash_str
from datetime import date

from model.user.user import User, UserRole
from schema.user.user import UserCreate, UserModify


def get_all_user(db, is_active):
    """
    Permite traer a todos los usuarios registrados en la base de datos
    """
    rows = db.query(User).filter_by(is_active=is_active).all()
    return rows


def get_user_by_id(db, user_id: int):
    """
    Permite consultar a un usuario en particular.

    Recibe: Id del usuario
    Regresa: El usuario con el id ingresado
    """
    return (
        db.query(User)
        .filter_by(
            id=user_id,
        )
        .first()
    )


def get_user_by_email(db, user_email: str):
    """
    Recibe un email del usuario 
    Regresa al usuario asociado con dicho email en caso de existir uno
    """
    return (
        db.query(User)
        .filter_by(
            email=user_email
        )
        .first()
    )


def create_new_user(db, new_user: UserCreate, user_role: UserRole):
    "Función para crear un usuario"
    db_user = None
    try:
        db_user = User(
            email = new_user.email, 
            hashed_pass=hash_str(new_user.hashed_pass),  
            is_active = new_user.is_active,
            created_at =new_user.created_at,
            role=user_role
            )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_user = None
        return db_user
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_user


def update_user_by_id(db, user_id: int, modify_user: UserModify):
    rows_updated = (
        db.query(User)
        .filter_by(id=user_id)
        .update(modify_user, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"status": True}
