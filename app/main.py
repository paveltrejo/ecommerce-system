from fastapi import FastAPI
from service.user.user import user_routes
from service.user.token import token_routes
from service.user.admin import admin_routes
from service.product.product import product_routes
from service.user.seller import seller_routes
from service.user.logistic import logistics_routes
from service.user.finantial import finantial_routes
app = FastAPI()

app.include_router(user_routes)
app.include_router(token_routes)
app.include_router(admin_routes)
app.include_router(seller_routes)
app.include_router(product_routes)
app.include_router(logistics_routes)
app.include_router(finantial_routes)


@app.post("/", )
def root_test():
    return "Cadena de prueba"