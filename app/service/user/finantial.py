from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime

from crud.product.product import get_payment_for_seller
from model.user import User

from utils.db import SessionLocal
from utils.email_validation import email_verification
from utils.functions_jwt import get_current_active_user


finantial_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los usuarios del sistema

@finantial_routes.get("/api/v1/finantial/payments/{seller_id}", tags = ["Finantial"])
def get_payment_seller(
        response: Response,
        seller_id: int, 
        month: int,
        year:int, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_payment_for_seller"
    
    if 'Financial' in current_user.role:
        response = get_payment_for_seller(db, seller_id, year, month)
        return response
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


    