from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.routes import categories, orders, products, users, carts
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

app.include_router(categories.router, prefix='/api/categories')
app.include_router(orders.router, prefix='/api/orders')
app.include_router(products.router, prefix='/api/products')
app.include_router(users.router, prefix='/api/users')
app.include_router(carts.router, prefix='/api/carts')

@app.get("/api")
def read_root():
    return {"message": "Bem vindo(a) ao MySportItens API"}