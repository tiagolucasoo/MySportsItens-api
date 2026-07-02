from fastapi import APIRouter, Depends
from api.services.auth import admin_only, all_users
from api.models.cart import Cart
from api.database import db
from datetime import datetime

router = APIRouter(tags=["Carts"], prefix="/carts")

@router.get("/{user_code}")
async def get_cart(user_code: str):
    cart = await db.carts.find_one({"userCode": user_code})
    
    if not cart:
        return {"userCode": user_code, "items": []}
    
    cart["_id"] = str(cart["_id"])
    return cart

@router.post("/")
async def insert_cart(cart: Cart, user = Depends(admin_only)):
    cart.updated_at = datetime.utcnow()
    cart_dict = cart.model_dump(by_alias=True, exclude_none=True)
    
    await db.carts.update_one(
        {"userCode": cart.user_code},
        {"$set": cart_dict},
        upsert=True
    )
    
    return {"message": "Carrinho sincronizado com sucesso!"}