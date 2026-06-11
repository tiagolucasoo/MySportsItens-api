from fastapi import FastAPI
from api.routes import categories, orders, products, users
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(categories.router, prefix='/api/categories')
#app.include_router(orders.router, prefix='/api/orders')
app.include_router(products.router, prefix='/api/products')
#app.include_router(users.router, prefix='/api/users')

@app.get("/api")
def read_root():
    return {"message": "Bem vindo(a) ao MySportItens API"}