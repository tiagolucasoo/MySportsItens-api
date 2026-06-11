from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class CartItem(BaseModel):
    product_sku: str = Field(alias="productSku")
    quantity: int

class Cart(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    user_code: str = Field(alias="userCode")
    items: List[CartItem] = []
    updated_at: datetime = Field(alias="updatedAt", default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}