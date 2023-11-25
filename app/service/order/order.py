from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from crud.order.order import (
    create_new_order, 
    get_order_by_id, 
    get_products_by_order_id,
    delete_order
)
from schema.order.order import (
    OrderCreate,
    OrderModify,
    OrderProductCreate
)
from model.order.order import Order, OrderStatus
from model.order.order_product import OrderProduct
from model.user.user import User

from utils.db import SessionLocal
from utils.email_validation import email_verification
from utils.functions_jwt import get_current_active_user

logistics_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los usuarios del sistema


@logistics_routes.post("/api/v1/logistics/orders/", tags=["Logistics"])
def create_order(
        new_order_prod: OrderProductCreate,
        status: OrderStatus,
        response: Response,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "create_new_order"

    if 'Logistic' in current_user.role:

        user = create_new_order(db, new_order_prod, status)
        if user is not None:
            return {"message": "Exitoso", "data": user}
        else:
            response.status_code = 401
            return {"message": "No se pudo guardar en la BD", "data": user}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


@logistics_routes.get("/api/v1/logistics/orders/{order_id}", tags=["Logistics"])
def get_order(order_id: int,
              response: Response,
              db: Session = Depends(get_db),
              current_user: User = Depends(get_current_active_user)):
    NAME = "get_order_complete"

    if 'Logistic' in current_user.role:
        order = get_order_by_id(db, order_id)
        products = get_products_by_order_id(db, order_id)
        return {
            "order": order,
            "products": products
        }

    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

@logistics_routes.delete("/api/v1/delete/logistics/orders/{order_id}", tags=["Logistics"])
def delete_user_by_id(
        response: Response,
        order_id:int, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "delete_user_by_id"

    if 'Logistic' in current_user.role:
        status = delete_order(db, order_id)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

