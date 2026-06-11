from fastapi import APIRouter
from api.models.cart import Cart
from api.database import db
from datetime import datetime

router = APIRouter()

@router.get("/{user_code}")
async def get_cart(user_code: str):
    cart = await db.carts.find_one({"userCode": user_code})
    
    if not cart:
        return {"userCode": user_code, "items": []}
    
    cart["_id"] = str(cart["_id"])
    return cart

@router.post("/")
async def upsert_cart(cart: Cart):
    cart.updated_at = datetime.utcnow()
    cart_dict = cart.model_dump(by_alias=True, exclude_none=True)
    
    await db.carts.update_one(
        {"userCode": cart.user_code},
        {"$set": cart_dict},
        upsert=True
    )
    
    return {"message": "Carrinho sincronizado com sucesso!"}