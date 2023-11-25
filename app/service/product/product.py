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

product_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Ruta para traer a todos los productos del sistema


@product_routes.get("/api/v1/products/", tags=["Products"])
def get_product(is_active: bool = True, db: Session = Depends(get_db)):
    NAME = "get_all_products"

    list_product = get_all_product(db, is_active)
    return {"data": list_product}

