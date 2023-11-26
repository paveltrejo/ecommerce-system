from sqlalchemy import case, and_, extract
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from utils.hash import hash_str
from datetime import date, datetime

from model.product.product import Product, ProductLog
from model.order import Order, OrderProduct
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
            id=product_id
        )
        .first()
    )

    return product


def create_new_prdouct_log(db, new_product_log:ProductCreate, product_id:int):
    db_product_log = None
    try:
        db_product_log = ProductLog(**new_product_log.dict(), product_id=product_id)
        db.add(db_product_log)
        db.commit()
        db.refresh(db_product_log)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_product_log = None
        return db_product_log
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_product_log



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


def update_product_by_id(db, product_id: int, modify_product: ProductModify, user_id: int):

    product = get_product_by_id(db, product_id, user_id)
    
    product_create = ProductCreate(
        name = product.name,
        description = product.description,
        price = product.price,
        status = product.status,
        owner_id = product.owner_id,
        is_active = product.is_active
    )
    product_log = create_new_prdouct_log(db, product_create, product_id)

    if product:
        rows_updated = (
            db.query(Product)
            .filter_by(id=product_id)
            .update(modify_product, synchronize_session="fetch")
        )
        db.commit()
        return rows_updated
    else:
        return 403


def delete_product(db: Session, product_id: int, user_id: int):

    product = get_product_by_id(db, product_id, user_id)
    if product:
        product = db.query(Product).filter(Product.id == product_id).first()
        db.delete(product)
        db.commit()
        return "Registro eliminado correctamente"
    else:
        return "No tienes acceso a borrar este registro "


def get_payment_for_seller(db: Session, seller_id: int, year: int, month: int):

    # order= db.query(Order.created_at).filter(Order.id==3).first()
    order_products = (
        db.query(
            OrderProduct.product_price.label("product_price"), 
            Product.name.label("product_name")
            )
        .join(Order, Order.id == OrderProduct.order_id)
        .join(Product, Product.id == OrderProduct.product_id)
        .filter(and_(
            Order.status == "Aprobada", 
            extract("month", Order.created_at) == month, 
            extract("year", Order.created_at) == year, 
            Product.owner_id == seller_id))
        .all()

    )
    if order_products:
        total_amount = 0
        products = []
        for order in order_products:
            total_amount = total_amount + order.product_price
            products.append({"product_name": order.product_name, "product_price": "$" + str( order.product_price)})
        return {
            "number_products_sold": len(products),
            "pay_for_seller": "$" + str(total_amount*0.90),
            "products_sold": products
         }
    else:
        return{
            "message": "El vendedor no tuvo ventas en este periodo de tiempo"
        }


def search_product_by_name(db: Session, search: str):
    possible_products = (
        db.query(
            Product
        )        
        .filter(
            Product.name.ilike(r"%{}%".format(search))
        )
        .all()
    )
    if possible_products:
        return possible_products
    else:
        return "No hay productos que coincidan con la busqueda"


def filter_product_by_status(db: Session, status: str):
    possible_products = (
        db.query(
            Product
        )        
        .filter(
            Product.status == status
        )
        .all()
    )
    if possible_products:
        return possible_products
    else:
        return "No hay productos que coincidan con la busqueda"

def filter_product_by_price(db: Session, min_price:int, max_price:int):
    possible_products=(
        db.query(Product)
        .filter(and_(Product.price >= min_price, Product.price <= max_price))
        .all()
    )
    if possible_products:
            return possible_products
    else:
        return "No hay productos que coincidan con la busqueda"

def get_product_log_by_id(db: Session, product_id:int):
    
    actual_product = db.query(Product).filter(Product.id == product_id).first()
    product_log = (
        db.query(ProductLog)
        .filter(ProductLog.product_id==product_id)
        .all()
    )

    return {
        "actual_product": actual_product,
        "product_log": product_log
    }