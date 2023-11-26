
from schema.user.user import UserCreate
from schema.product.product import ProductCreate
from crud.user.user import create_new_user
from crud.product.product import create_new_product



def create_data_db(db):

    buyer_user = UserCreate(
        email = "buyer@gmail.com",
        hashed_pass = "string",
        is_active = True
    )

    admin_user = UserCreate(
        email = "admin@gmail.com",
        hashed_pass = "string",
        is_active = True
    )

    finantial_user = UserCreate(
        email = "finantial@gmail.com",
        hashed_pass = "string",
        is_active = True
    )

    logistic_user = UserCreate(
        email = "logistic@gmail.com",
        hashed_pass = "string",
        is_active = True
    )

    seller_user1 = UserCreate(
        email = "seller1@gmail.com",
        hashed_pass = "string",
        is_active = True
    )

    seller_user2 = UserCreate(
        email = "seller2@gmail.com",
        hashed_pass = "string",
        is_active = True
    )




    create_new_user(db, buyer_user, "Buyer")
    create_new_user(db, admin_user, "Admin")
    create_new_user(db, finantial_user, "Financial")
    create_new_user(db, seller_user1, "Seller")
    create_new_user(db, seller_user2, "Seller")

    print("************** Usuarios Creados ************************************")

    


    print("************** Productos Creados ************************************")

    new_product1 = ProductCreate(
        name = "producto1",
        description = "descripcion de producto1",
        price = 2000,
        is_active =  True
    )
    new_product2 = ProductCreate(
        name = "producto2",
        description = "descripcion de producto2",
        price = 3000.15,
        is_active =  True
    )
    new_product3 = ProductCreate(
        name = "producto3",
        description = "descripcion de producto3",
        price = 2500,
        is_active =  True
    )
    new_product4 = ProductCreate(
        name = "producto4",
        description = "descripcion de producto4",
        price = 300.05,
        is_active =  True
    )
    new_product5 = ProductCreate(
        name = "producto5",
        description = "descripcion de producto5",
        price = 4000,
        is_active =  True
    )
    new_product6 = ProductCreate(
        name = "producto6",
        description = "descripcion de producto6",
        price = 5500.99,
        is_active =  True
    )


    create_new_product(db, new_product1, 4)
    create_new_product(db, new_product2, 4)
    create_new_product(db, new_product3, 4)

    create_new_product(db, new_product4, 5)
    create_new_product(db, new_product5, 5)
    create_new_product(db, new_product6, 5)
    print("************** Productos Creados ************************************")

    return {"message": "success"}