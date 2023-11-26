from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from crud.product.product import (
    get_all_product,
    search_product_by_name,
    filter_product_by_status,
    filter_product_by_price
)
from schema.product.product import (
    ProductCreate,
    ProductModify
)
from model.product.product import Product, ProductStatus
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

@product_routes.get("/api/v1/products/search/name/{search}", tags=["Products"])
def get_search_product_by_name(search:str, db: Session = Depends(get_db)):
    possible_products  = search_product_by_name(db, search)
    return { "data": possible_products }

@product_routes.get("/api/v1/products/filter/status/{search}", tags=["Products"])
def get_filter_product_by_status(status:ProductStatus, db: Session = Depends(get_db)):
    possible_products  = filter_product_by_status(db, status)
    return { "data": possible_products }

@product_routes.get("/api/v1/products/filter/price/", tags=["Products"])
def get_filter_product_by_price(min_price:float, max_price:float, db: Session = Depends(get_db)):
    possible_products  = filter_product_by_price(db, min_price, max_price)
    return { "data": possible_products }