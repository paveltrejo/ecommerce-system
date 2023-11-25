from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from crud.user.user import (
    get_all_user,
    get_user_by_id,
    get_user_by_email,
    update_user_by_id,
    create_new_user,
    delete_user
)
from schema.user.user import (
    UserCreate,
    UserModify
)
from model.user.user import UserRole

from utils.db import SessionLocal

user_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los usuarios del sistema


@user_routes.get("/api/v1/users/", tags=["Users"])
def get_user(is_active: bool = True, db: Session = Depends(get_db)):
    NAME = "get_all_users"

    list_user = get_all_user(db, is_active)
    return {"data": list_user}

# Ruta para traer a un usuario por su id


@user_routes.get("/api/v1/users/{user_id}", tags=["Users"])
def get_user_by__id(user_id: str, db: Session = Depends(get_db)):
    NAME = "get_user_by_id"

    user = get_user_by_id(db, user_id)
    return {"data": user}

# Ruta para crear un nuevo usuario


@user_routes.post("/api/v1/users/", tags=["Users"])
def create_user(user_role: UserRole, new_user: UserCreate, response: Response, db: Session = Depends(get_db)):
    NAME = "create_new_user"

    exist_email = get_user_by_email(db, new_user.email)

    if exist_email:
        response.status_code = 401
        return {"message": "El correo ya esta registrado en el sistema. Utiliza uno nuevo"}

    user = create_new_user(db, new_user, user_role)
    if user is not None:
        return {"message": "Exitoso", "data": user}
    else:
        response.status_code = 401
        return {"message": "No se pudo guardar en la BD", "data": user}

# Ruta para actualizar a un nuevo usuario por medio de su id


@user_routes.patch("/api/v1/users/{user_id}", tags=["Users"])
def update_user(user_id: str, modify_user: UserModify, response: Response, db: Session = Depends(get_db)):
    NAME = "update_user_by_id"

    update_data = modify_user.dict(exclude_unset=True)
    user_update_result = update_user_by_id(db, user_id, update_data)

    if user_update_result != 0:
        exist_user = get_user_by_id(db, user_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_user}
    else:
        response.status_code = 401
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

# Ruta para borrar un usuario por medio de su id


@user_routes.delete("/api/v1/delete/users/{user_id}", tags=["Users"])
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    NAME = "delete_user_by_id"

    status = delete_user(db, user_id)
    return {"message": status}
