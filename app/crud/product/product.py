from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from utils.hash import hash_str
from datetime import date

from model.product.product import Product
from schema.product.product import ProductCreate, ProductModify


def get_all_product(db, is_active):
    """
    Permite traer a todos los productos registrados en la base de datos con status
    de activo
    """
    rows = db.query(Product).filter_by(is_active=is_active).all()
    return rows


def get_product_by_id(db, product_id: int):
    """
    Permite consultar a un producto en particular.

    Recibe: Id del producto
    Regresa: El producto con el id ingresado
    """
    return (
        db.query(Product)
        .filter_by(
            id=product_id,
        )
        .first()
    )


def get_product_by_email(db, product_email: str):
    """
    Recibe un email del producto 
    Regresa al producto asociado con dicho email en caso de existir uno
    """
    return (
        db.query(Product)
        .filter_by(
            email=product_email
        )
        .first()
    )


def create_new_product(db, new_product: ProductCreate):
    "Función para crear un producto"
    db_product = None
    try:
        db_product = Product(**new_product.dict()
            )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_product = None
        return db_product
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_product


def update_product_by_id(db, product_id: int, modify_product: ProductModify):
    rows_updated = (
        db.query(Product)
        .filter_by(id=product_id)
        .update(modify_product, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(product)
    db.commit()
    return {"status": True}
