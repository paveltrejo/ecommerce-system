from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime

from crud.order.order import (
    create_new_order,
    get_all_order,
    get_order_by_id,
    get_products_by_order_id,
    update_order_by_id,
    change_status_order_by_id,
    change_eta_order_by_id,
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


@logistics_routes.get("/api/v1/orders/", tags=["Logistics"])
def get_order(
        response: Response,
        is_active: bool = True,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "get_all_orders"
    if 'Logistic' in current_user.role:
        list_order = get_all_order(db, is_active)
        return {"data": list_order}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


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


@logistics_routes.patch("/api/v1/logistics/orders/{order_id}", tags=["Logistics"])
def update_user(
        order_id: int,
        modify_order: OrderModify,
        response: Response,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "update_order_by_id"

    if 'Logistic' in current_user.role:
        update_data = modify_order.dict(exclude_unset=True)
        user_update_result = update_order_by_id(db, order_id, update_data)

        if user_update_result != 0:
            exist_order = get_order_by_id(db, order_id)
            return {"mensaje": "Actualizado Correctamente", "data": exist_order}
        else:
            response.status_code = 401
            return {"mensaje": "Ningun registro fue afectado", "data": ""}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


@logistics_routes.patch("/api/v1/logistics/orders/approve/{order_id}", tags=["Logistics"])
def approve_order(
        response: Response,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "approve_order_by_id"

    if 'Logistic' in current_user.role:
        status = change_status_order_by_id(db, order_id, 1)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


@logistics_routes.patch("/api/v1/logistics/orders/reject/{order_id}", tags=["Logistics"])
def reject_order(
        response: Response,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "approve_order_by_id"

    if 'Logistic' in current_user.role:
        status = change_status_order_by_id(db, order_id, 2)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


@logistics_routes.patch("/api/v1/logistics/orders/eta/{order_id}", tags=["Logistics"])
def update_eta_order(
        response: Response,
        order_id: int,
        eta: datetime,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "change_eta_order_by_id"

    if 'Logistic' in current_user.role:
        status = change_eta_order_by_id(db, order_id, eta)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


@logistics_routes.delete("/api/v1/logistics/delete/orders/{order_id}", tags=["Logistics"])
def delete_user_by_id(
        response: Response,
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    NAME = "delete_order_by_id"

    if 'Logistic' in current_user.role:
        status = delete_order(db, order_id)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}
