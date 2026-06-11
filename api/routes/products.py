from fastapi import APIRouter
from api.models.product import Product
from api.database import db

router = APIRouter()

@router.get("/")
async def list_products():
    products = await db.products.find().to_list(length=100)
    
    for product in products:
        product["_id"] = str(product["_id"])
        
    return products

@router.post("/")
async def create_product(product: Product):
    new_product = await db.products.insert_one(product.model_dump(by_alias=True, exclude_none=True))
    return {"id": str(new_product.inserted_id)}