from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from utils.hash import hash_str
from datetime import date, datetime

from model.order.order import Order, OrderStatus
from model.order.order_product import OrderProduct
from model.product.product import Product
from schema.order.order import OrderCreate, OrderModify, OrderProductCreate
from crud.product.product import get_product_id

def get_all_order(db, is_active:bool =True):
    return(
        db.query(Order).filter(Order.is_active==is_active).all()
    )

def create_new_order(db, new_order: OrderProductCreate, status_order: str):
    "Función para crear una orden de compra"
    db_order = None
    db_orderproduct = None
    total_amount = 0
    try:
        db_order = Order(**new_order.order.dict(), status=status_order)
        db.add(db_order)
        db.commit()
        for product in new_order.products_id:
            product_item = get_product_id(db, product)
            db_orderproduct = OrderProduct(
                order_id=db_order.id, product_id=product, product_price=product_item.price)
            total_amount = total_amount + product_item.price
            db.add(db_orderproduct)
            db.commit()
        status = (db.query(Order).filter(Order.id == db_order.id).update(
            {"total_amount": total_amount}))
        db.commit()
        db.refresh(db_order)

    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_order = None
        return db_order
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_order


def get_order_by_id(db, order_id: int):
    """
    Permite consultar a un usuario en particular.
    Recibe: Id del usuario
    Regresa: El usuario con el id ingresado
    """
    order = (
        db.query(Order)
        .filter_by(id=order_id)
        .first()
    )

    return order


def get_products_by_order_id(db, order_id: int):

    products = (
        db.query(Product.name.label("product_name"),
                 Product.price.label("product_price"))
        .select_from(OrderProduct)
        .join(Product, Product.id == OrderProduct.product_id)
        .filter(OrderProduct.order_id == order_id)
        .all()
    )
    return db_mapping_rows_to_dict(products)


def get_order_products_by_order_id(db, order_id: int):
    order_products = (
        db.query(OrderProduct)
        .filter(OrderProduct.order_id == order_id)
        .all()
    )
    return order_products


def update_order_by_id(db, order_id: int, modify_order: OrderModify):

    rows_updated = (
        db.query(Order)
        .filter_by(id=order_id)
        .update(modify_order, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def change_status_order_by_id(db, order_id: int, status: int):
    """
    Función que re define el status de una orden. Dependiendo el numero que reciba
    en status es el status que actualizara en la orden de order_id
    - Recibe: 
        order_id = Id de la orden a modificar
        status = Dependiendo el numero es el status que se actualizara en la orden
            1: Approval
            2: Rejection
    - Devuelve:
       row_update: Status 1 si la actualización fue exitosa
    """
    if status == 1:
        new_status = OrderStatus.approval.value
    elif status == 2:
        new_status = OrderStatus.rejection.value
    else: 
        return 404
    
    row_update = (
        db.query(Order)
        .filter_by(id=order_id)
        .update({"status": new_status})
    )
    db.commit()

    return row_update

def change_eta_order_by_id(db, order_id:int, eta: datetime):
    """
    Función que actualiza la fecha de entrega estimada par auna orden
    - Recibe: La fecha de eta y el id de la orden
    - Regresa: Status 1 si la actualización fue exitosa
    """

    row_update = (
        db.query(Order)
        .filter_by(id=order_id)
        .update({"eta": eta})
    )
    db.commit()
    return row_update



def delete_order(db: Session, order_id: int):

    orders_product = get_order_products_by_order_id(db, order_id)
    for order_product in orders_product:
        db.delete(order_product)
        db.commit()

    order = get_order_by_id(db, order_id)
    if order:
        order = db.query(Order).filter(Order.id == order_id).first()
        db.delete(order)
        db.commit()
        return "Registro eliminado correctamente"
    else:
        return "No tienes acceso a borrar este registro "
