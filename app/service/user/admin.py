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
from crud.product.product import get_product_log_by_id
from crud.order.order import get_order_log_by_id
from schema.user.user import (
    UserCreate,
    UserModify
)
from model.user.user import UserRole, UserRoleSignUp, User

from utils.db import SessionLocal
from utils.email_validation import email_verification
from utils.functions_jwt import get_current_active_user
from utils.create_data import create_data_db
from utils.test import test

admin_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los usuarios del sistema


@admin_routes.get("/api/v1/admin/users/", tags=["Admin"])
def get_user(
        response: Response,
        is_active: bool = True,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_all_users"

    print("#####################################")
    print(current_user)

    if 'Admin' in current_user.role:
        list_user = get_all_user(db, is_active)
        return {"data": list_user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

# Ruta para traer a un usuario por su id


@admin_routes.get("/api/v1/admin/users/{user_id}", tags=["Admin"])
def get_user_by__id(
        response: Response,
        user_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_user_by_id"
    if 'Admin' in current_user.role:
        user = get_user_by_id(db, user_id)
        return {"data": user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}
# Ruta para crear un nuevo usuario


@admin_routes.post("/api/v1/admin/users/", tags=["Admin"])
def create_user(
        user_role: UserRole,
        new_user: UserCreate,
        response: Response, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "create_new_user"

    if 'Admin' in current_user.role:
        exist_email = get_user_by_email(db, new_user.email)
        if exist_email:
            response.status_code = 401
            return {"message": "El correo ya esta registrado en el sistema. Utiliza uno nuevo"}

        # email_status = email_verification(new_user.email)
        # if email_status['is_free_email']['value'] is False:
        #    response.status_code = 403
        #    return{"message": "El correo se encuentra en la lista negra de correos"}

        user = create_new_user(db, new_user, user_role)
        if user is not None:
            return {"message": "Exitoso", "data": user}
        else:
            response.status_code = 401
            return {"message": "No se pudo guardar en la BD", "data": user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

# Ruta para actualizar a un nuevo usuario por medio de su id


@admin_routes.patch("/api/v1/admin/users/{user_id}", tags=["Admin"])
def update_user(
        user_id: str,
        modify_user: UserModify,
        response: Response,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "update_user_by_id"

    if 'Admin' in current_user.role:
        update_data = modify_user.dict(exclude_unset=True)
        user_update_result = update_user_by_id(db, user_id, update_data)

        if user_update_result != 0:
            exist_user = get_user_by_id(db, user_id)
            return {"mensaje": "Actualizado Correctamente", "data": exist_user}
        else:
            response.status_code = 401
            return {"mensaje": "Ningun registro fue afectado", "data": ""}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

# Ruta para borrar un usuario por medio de su id


@admin_routes.delete("/api/v1/delete/admin/users/{user_id}", tags=["Admin"])
def delete_user_by_id(
        response: Response,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "delete_user_by_id"

    if 'Admin' in current_user.role:
        status = delete_user(db, user_id)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


@admin_routes.get("/api/v1/admin/products/log/{product_id}", tags=["Admin"])
def get_product_log(
        response: Response,
        product_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_product_log_by_id"
    if 'Admin' in current_user.role:
        product_log = get_product_log_by_id(db, product_id)
        return {"data": product_log}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

@admin_routes.get("/api/v1/admin/orders/log/{order_id}", tags=["Admin"])
def get_order_log(
        response: Response,
        order_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_product_log_by_id"
    if 'Admin' in current_user.role:
        order_log = get_order_log_by_id(db, order_id)
        return {"data": order_log}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

@admin_routes.get("/api/v1/create/data/db/", tags=["db"])
def create_data_in_db(db: Session = Depends(get_db)):
    status = create_data_db(db)
    return status


@admin_routes.get("/api/v1/test/", tags=["Test"])
def create_data_in_db(db: Session = Depends(get_db)):
    status = test(db)
    return status
