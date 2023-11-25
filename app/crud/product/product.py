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


def get_all_product_by_seller(db, is_active, seller_id: int):
    """
    Permite consultar a un producto en particular.

    Recibe: Id del Seller
    Regresa: Los productos pertenecientes al seller
    """
    return (
        db.query(Product)
        .filter(and_(
            Product.owner_id == seller_id,
            Product.is_active == is_active
        )
        )
        .all()
    )


def get_product_by_id(db, product_id: int, seller_id: int):
    """
    Permite consultar a un producto en particular.

    Recibe: Id del producto
    Regresa: El producto con el id ingresado
    """
    product = (
        db.query(Product)
        .filter(and_(
            Product.id == product_id,
            Product.owner_id == seller_id
        ))
        .first()
    )

    return product

def get_product_id(db, product_id: int):
    """
    Permite consultar a un producto en particular.

    Recibe: Id del producto
    Regresa: El producto con el id ingresado
    """
    product = (
        db.query(Product)
        .filter_by(
            id = product_id
        )
        .first()
    )

    return product


def create_new_product(db, new_product: ProductCreate, user_id: int):
    "Función para crear un producto"
    db_product = None
    try:
        db_product = Product(owner_id=user_id,
                             name=new_product.name,
                             description=new_product.description,
                             price=new_product.price,
                             is_active=new_product.is_active,
                             created_at=new_product.created_at
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


def update_product_by_id(db, product_id: int, modify_product: ProductModify, user_id:int):
    
    product = get_product_by_id(db, product_id, user_id)
    print("#####################################")
    print(product)
    if product:
        rows_updated = (
            db.query(Product)
            .filter_by(id=product_id)
            .update(modify_product, synchronize_session="fetch")
        )
        db.commit()
        return rows_updated
    else: 
        print("Si entre")
        return 403


def delete_product(db: Session, product_id: int, user_id:int):
    
    product = get_product_by_id(db, product_id, user_id)
    if product:
        product = db.query(Product).filter(Product.id == product_id).first()
        db.delete(product)
        db.commit()
        return "Registro eliminado correctamente"
    else: 
        return "No tienes acceso a borrar este registro "
