from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.routes import categories, orders, products, users, carts
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(
    title="MySportItens API",
    description="API para gerenciamento de produtos esportivos, categorias, pedidos e usuários.",
    version="1.0.0",
    contact={
        "name": "Tiago Lucas (GitHub: Tiagolucasoo)",
        "url": "https://www.linkedin.com/in/tiagoollucas"
    },
    openapi_tags=[
        {
            "name": "API",
            "description": "Informações gerais da API"
        },
        {
            "name": "Categories",
            "description": "Operações com categorias"
        },
        {
            "name": "Products",
            "description": "Operações com produtos"
        },
        {
            "name": "Orders",
            "description": "Operações com pedidos"
        },
        {
            "name": "Users",
            "description": "Operações com usuários"
        },
        {
            "name": "Carts",
            "description": "Operações com carrinhos"
        }
    ]
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

app.include_router(categories.router, prefix='/api/categories')
app.include_router(orders.router, prefix='/api/orders')
app.include_router(products.router, prefix='/api/products')
app.include_router(users.router, prefix='/api/users')
app.include_router(carts.router, prefix='/api/carts')

@app.get("/api", tags=["API"])
def read_root():
    return {
        "name": "MySportItens API",
        "version": "1.0.0",
        "message": "Bem vindo(a) ao MySportItens API",
        "context": (
            "Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento "
            "de Aplicações para Dispositivos Móveis (IFPR - Campus Londrina), "
            "utilizando React Native no aplicativo e FastAPI na API."
        ),
        "github": {
            "api": "https://github.com/tiagolucasoo/mysportsitens-api",
            "app": "https://github.com/mribeirom/my-sport-itens"
        },
        "routes": {
            "categories": "/api/categories",
            "products": "/api/products",
            "orders": "/api/orders",
            "users": "/api/users",
            "carts": "/api/carts"
        }
    }