from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class Product(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    sku: str
    name: str
    description: str
    image_url: str = Field(alias="imageUrl")
    category_slug: str = Field(alias="categorySlug")
    price: float
    stock: int = 0
    active: bool = True
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}