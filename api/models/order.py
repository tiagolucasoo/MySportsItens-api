from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class OrderItem(BaseModel):
    product_sku: str = Field(alias="productSku")
    name: str
    image_url: str = Field(alias="imageUrl")
    unit_price: float = Field(alias="unitPrice")
    quantity: int
    total: float

class Order(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    code: str
    user_code: str = Field(alias="userCode")
    items: List[OrderItem]
    total_amount: float = Field(alias="totalAmount")
    status: str = "paid"
    payment_code: str = Field(alias="paymentCode")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}