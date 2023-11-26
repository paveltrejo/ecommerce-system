from crud.order.order import (
    create_new_order, 
    change_eta_order_by_id, 
    change_status_order_by_id
    )

from crud.product.product import (
    get_payment_for_seller, 
    update_product_by_id, 
    get_product_by_id, 
    delete_product
    )
from schema.order.order import OrderCreate, OrderProductCreate
from schema.product.product import ProductModify
from datetime import datetime


def test(db):
    products_id = [2,3,5]
    new_order = OrderCreate(
        buyer_id = 1,
        eta = datetime.now(),
        is_active = True,
    )
    new_order_product = OrderProductCreate(
        order = new_order,
        products_id = products_id
    )
    create_new_order(db, new_order_product, "Rechazada")

    print("******************* Orden Creada Por El Comprador *****************")

    change_status_order_by_id(db, 1, 1)
    
    print("******************* Logistict acepta la orden *****************")

    data1 = get_payment_for_seller(db, 4, 2023, 11)

    data2 = get_payment_for_seller(db, 5, 2023, 11)

    print("******************* Financial obtiene pagos a sellers *****************")
    print(data1)
    print(data2)

    change_eta_order_by_id(db, 1, "2023-12-01T12:00:00")

    print("******************* Logistic cambia fecha de entrega *****************")

    product= get_product_by_id(db, 2, 4)
    modify_product = {
        "name" : product.name,
        "description" : product.description, 
        "owner_id" : 4,
        "price" : 230.15,
        "is_active" : product.is_active
    }
    update_product_by_id(db, 2, modify_product, 4)
    print("******************* Seller cambia precio de producto *****************")

    change_eta_order_by_id(db, 1, "2023-12-03T12:00:00")

    print("******************* Logistic cambia fecha de entrega por segunda vez*****************")


    delete_product(db, 3, 4)

    print("****************** Seller borra un producto **************************************")


    product= get_product_by_id(db, 5, 5)
    modify_product = {
        "name" : product.name,
        "description" : product.description, 
        "owner_id" : 5,
        "price" : 230.15,
        "is_active" : product.is_active
    }
    update_product_by_id(db, 5, modify_product, 5)
    print("******************* Seller cambia precio de producto por segunda ocación*****************")

    return {"message": "success"}