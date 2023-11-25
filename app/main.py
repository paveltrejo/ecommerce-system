from fastapi import FastAPI
from service.user.user import user_routes
app = FastAPI()

app.include_router(user_routes)

@app.post("/", )
def root_test():
    return "Cadena de prueba"