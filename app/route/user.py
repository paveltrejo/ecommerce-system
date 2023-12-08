from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from service_new.user import UserService

from schema.user.user import (
    UserCreate,
    UserModify
)
from model.user.user import UserRole, User

from utils.db import SessionLocal

from utils.functions_jwt import get_current_active_user

admin_routes_changes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los usuarios del sistema


@admin_routes_changes.get("/api/v1/admin2/users/", tags=["Admin Nueva Estructura"])
def get_user(
        response: Response,
        is_active: bool = True,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_all_users"
    u_serv = UserService(db)
    if 'Admin' in current_user.role:
        list_user = u_serv.get_all_users(is_active)
        return {"data": list_user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

# Ruta para traer a un usuario por su id


@admin_routes_changes.get("/api/v1/admin2/users/{user_id}", tags=["Admin Nueva Estructura"])
def get_user_by__id(
        response: Response,
        user_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_user_by_id"
    u_serv = UserService(db)
    if 'Admin' in current_user.role:
        user = u_serv.get_user_by_id(user_id)
        return {"data": user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}
# Ruta para crear un nuevo usuario


@admin_routes_changes.post("/api/v1/admin2/users/", tags=["Admin Nueva Estructura"])
def create_user(
        user_role: UserRole,
        new_user: UserCreate,
        response: Response, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "create_new_user"
    u_serv = UserService(db)
    if 'Admin' in current_user.role:
        exist_email = u_serv.get_user_by_email(new_user.email)
        if exist_email:
            response.status_code = 401
            return {"message": "El correo ya esta registrado en el sistema. Utiliza uno nuevo"}
        user = u_serv.create_user(new_user, user_role)
        if user is not None:
            return {"message": "Exitoso", "data": user}
        else:
            response.status_code = 401
            return {"message": "No se pudo guardar en la BD", "data": user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

# Ruta para actualizar a un nuevo usuario por medio de su id


@admin_routes_changes.patch("/api/v1/admin2/users/{user_id}", tags=["Admin Nueva Estructura"])
def update_user(
        user_id: str,
        modify_user: UserModify,
        response: Response,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "update_user_by_id"
    u_serv = UserService(db)
    if 'Admin' in current_user.role:
        update_data = modify_user.dict(exclude_unset=True)
        user_update_result = u_serv.update_user(user_id, update_data)

        if user_update_result != 0:
            exist_user = u_serv.get_user_by_id(user_id)
            return {"mensaje": "Actualizado Correctamente", "data": exist_user}
        else:
            response.status_code = 401
            return {"mensaje": "Ningun registro fue afectado", "data": ""}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

# Ruta para borrar un usuario por medio de su id


@admin_routes_changes.delete("/api/v1/delete/admin2/users/{user_id}", tags=["Admin Nueva Estructura"])
def delete_user_by_id(
        response: Response,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "delete_user_by_id"
    u_serv = UserService(db)
    if 'Admin' in current_user.role:
        status = u_serv.delete_user(user_id)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}
