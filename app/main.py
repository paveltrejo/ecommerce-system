from fastapi import FastAPI
from service.user.user import user_routes
from service.user.token import token_routes
from service.user.admin import admin_routes
app = FastAPI()

app.include_router(user_routes)
app.include_router(token_routes)
app.include_router(admin_routes)

@app.post("/", )
def root_test():
    return "Cadena de prueba"