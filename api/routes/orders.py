from fastapi import APIRouter
from api.models.order import Order
from api.database import db
import uuid

router = APIRouter()

@router.get("/{user_code}")
async def list_user_orders(user_code: str):
    orders = await db.orders.find({"userCode": user_code}).sort("createdAt", -1).to_list(length=100)
    
    for order in orders:
        order["_id"] = str(order["_id"])
        
    return orders

@router.post("/")
async def create_order(order: Order):
    if not order.code or order.code == "":
        order.code = f"ORDER-{uuid.uuid4().hex[:6].upper()}"

    new_order = await db.orders.insert_one(order.model_dump(by_alias=True, exclude_none=True))
    
    return {
        "id": str(new_order.inserted_id), 
        "code": order.code,
        "message": "Pedido gerado com sucesso!"
    }