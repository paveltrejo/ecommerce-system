from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from crud.product.product import (
    get_all_product_by_seller,
    get_product_by_id,
    update_product_by_id,
    create_new_product,
    delete_product
)
from schema.product.product import (
    ProductCreate,
    ProductModify
)
from model.product.product import Product
from model.user.user import User

from utils.db import SessionLocal
from utils.functions_jwt import get_current_active_user


seller_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Ruta para traer a todos los productos del seller
@seller_routes.get("/api/v1/seller/products/", tags=["Sellers"])
def get_product(response: Response, is_active: bool = True, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    NAME = "get_all_products"
    if 'Seller' in current_user.role:
        list_product = get_all_product_by_seller(db, is_active, current_user.id)
        return {"data": list_product}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


# Ruta para traer a un producto por su id
@seller_routes.get("/api/v1/products/{product_id}", tags=["Sellers"])
def get_product_by__id(response: Response, product_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    NAME = "get_product_by_id"
    
    if 'Seller' in current_user.role:
        product = get_product_by_id(db, product_id, current_user.id)
        return {"data": product}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


# Ruta para crear un nuevo producto
@seller_routes.post("/api/v1/products/", tags=["Sellers"])
def create_product(response: Response, new_product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    NAME = "create_new_product"

    if 'Seller' in current_user.role:
        product = create_new_product(db, new_product, current_user.id)
        if product is not None:
            return {"message": "Exitoso", "data": product}
        else:
            response.status_code = 401
            return {"message": "No se pudo guardar en la BD", "data": product}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}


# Ruta para actualizar a un nuevo producto por medio de su id
@seller_routes.patch("/api/v1/products/{product_id}", tags=["Sellers"])
def update_product(response: Response, product_id: str, modify_product: ProductModify, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    NAME = "update_product_by_id"
    if 'Seller' in current_user.role:
        update_data = modify_product.dict(exclude_unset=True)
        product_update_result = update_product_by_id(db, product_id, update_data, current_user.id)

        if product_update_result != 403 :
            exist_product = get_product_by_id(db, product_id, current_user.id)
            return {"mensaje": "Actualizado Correctamente", "data": exist_product}
        else:
            response.status_code = 403
            return {"message": "No tienes acceso a esta información"}   
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}
   


# Ruta para borrar un producto por medio de su id
@seller_routes.delete("/api/v1/delete/products/{product_id}", tags=["Sellers"])
def delete_product_by_id(response: Response, product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    NAME = "delete_product_by_id"
    if 'Seller' in current_user.role:
        status = delete_product(db, product_id, current_user.id)
        return {"message": status}
    else:
        response.status_code = 403
        return {"message": "No tienes acceso a esta información"}

