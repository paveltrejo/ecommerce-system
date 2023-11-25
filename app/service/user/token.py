from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Response
from jose import jwt
from sqlalchemy.orm import Session

from crud.user.user import get_user_by_email 
from schema.user.token import Token, TokenRefresh, TokenCreate
from utils.db import SessionLocal
from utils.functions_jwt import validate_token, create_access_token, generate_new_tokens
from utils.hash import verify_str_hash

SECRET_KEY = "39d87423287d550c71e16d02fa7c4a522752a20bed9c505740b13aceeab5bf8a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 35

token_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_user(db, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return 2
    if not verify_str_hash(password, user.hashed_pass):
        return 3
    return user


@token_routes.post("/api/v1/users/login/", response_model=Token, tags=["Users"])
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: TokenCreate = Depends()
):
    """
    Status de login:
        - Si el detail es 1 el login fue exitoso, el usuario y contraseña son
          correctos.
        - Si el detail es 2 el login fue incorrecto, el usuario no existe
        - Si el detail es 3 el login fue incorrecto, la contraseña es inco-
          rrecta.
    """
    user = authenticate_user(db, form_data.username, form_data.password)

    if user == 2:
        detail = "El usuario no existe"
        raise HTTPException(
            status_code=404,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif user == 3:
        detail = "Contraseña incorrecta"
        raise HTTPException(
            status_code=403,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "user_email": user.email,
            "user_id": user.id,
            "user_active": user.is_active,
            "role_name": user.role,
            "access_token_expires": str(access_token_expires),
            "refresh_token_expires": str(refresh_token_expires),
        },
        expires_delta=access_token_expires,
    )
    refresh_token = create_access_token(
        data={
            "user_email": user.email,
            "user_id": user.id,
            "user_active": user.is_active,
            "role_name": user.role,
            "access_token_expires": str(access_token_expires),
            "refresh_token_expires": str(refresh_token_expires),
        },
        expires_delta=refresh_token_expires,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "detail": 1,
    }


@token_routes.post("/refresh/token", tags=["Token"])
async def refresh_access_token(
    token_refresh_data: TokenRefresh,
    db: Session = Depends(get_db),
    response: Response = 200,
):
    status_token, respuesta = validate_token(token_refresh_data.access_token)


    if status_token == 403:
        # realiza Verificacion del token Refresh
        response.status_code = 403
        status_token, respuesta = validate_token(token_refresh_data.refresh_token)
        if status_token == 403:
            response.status_code = 401
            respuesta = {
                "mensaje": "Ambos tokens estan expirados, no se puede refrescar",
                "data": [],
            }
        elif status_token == 200:
            response.status_code = 200
            respuesta = generate_new_tokens(db, respuesta.username)
        else:
            response.status_code = 401
    elif status_token == 200:
        # print(respuesta.username)
        respuesta = generate_new_tokens(db, respuesta.username)
    else:
        response.status_code = 401

    return respuesta
