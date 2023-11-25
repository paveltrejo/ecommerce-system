from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from crud.product.product import (
    get_all_product,
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

from utils.db import SessionLocal


seller_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los productos del seller


@seller_routes.get("/api/v1/seller/products/", tags=["Sellers"])
def get_product(is_active: bool = True, db: Session = Depends(get_db)):
    NAME = "get_all_products"

    list_product = get_all_product(db, is_active)
    return {"data": list_product}

# Ruta para traer a un usuario por su id


@seller_routes.get("/api/v1/products/{product_id}", tags=["Products"])
def get_product_by__id(product_id: str, db: Session = Depends(get_db)):
    NAME = "get_product_by_id"

    product = get_product_by_id(db, product_id)
    return {"data": product}

# Ruta para crear un nuevo usuario


@seller_routes.post("/api/v1/products/", tags=["Products"])
def create_product(new_product: ProductCreate, response: Response, db: Session = Depends(get_db)):
    NAME = "create_new_product"

    
    product = create_new_product(db, new_product)
    if product is not None:
        return {"message": "Exitoso", "data": product}
    else:
        response.status_code = 401
        return {"message": "No se pudo guardar en la BD", "data": product}

# Ruta para actualizar a un nuevo usuario por medio de su id


@seller_routes.patch("/api/v1/products/{product_id}", tags=["Products"])
def update_product(product_id: str, modify_product: ProductModify, response: Response, db: Session = Depends(get_db)):
    NAME = "update_product_by_id"

    update_data = modify_product.dict(exclude_unset=True)
    product_update_result = update_product_by_id(db, product_id, update_data)

    if product_update_result != 0:
        exist_product = get_product_by_id(db, product_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_product}
    else:
        response.status_code = 401
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

# Ruta para borrar un usuario por medio de su id


@seller_routes.delete("/api/v1/delete/products/{product_id}", tags=["Products"])
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    NAME = "delete_product_by_id"

    status = delete_product(db, product_id)
    return {"message": status}


