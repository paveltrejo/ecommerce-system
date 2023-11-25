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
from model.user.user import UserRole, UserRoleSignUp

from utils.db import SessionLocal
from utils.email_validation import email_verification

user_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Ruta para crear un nuevo usuario


@user_routes.post("/api/v1/users/sign_up/", tags=["Users"])
def create_user(user_role: UserRoleSignUp, new_user: UserCreate, response: Response, db: Session = Depends(get_db)):
    NAME = "create_new_user"

    exist_email = get_user_by_email(db, new_user.email)

    if exist_email:
        response.status_code = 401
        return {"message": "El correo ya esta registrado en el sistema. Utiliza uno nuevo"}

    #email_status = email_verification(new_user.email)
    #if email_status['is_free_email']['value'] is False:
    #    response.status_code = 403
    #    return{"message": "El correo se encuentra en la lista negra de correos"}

    user = create_new_user(db, new_user, user_role)
    if user is not None:
        return {"message": "Exitoso", "data": user}
    else:
        response.status_code = 401
        return {"message": "No se pudo guardar en la BD", "data": user}

# Ruta para actualizar a un nuevo usuario por medio de su id



