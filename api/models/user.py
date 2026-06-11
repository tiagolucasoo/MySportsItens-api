from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    code: str
    name: str
    email: str
    password_hash: str = Field(alias="passwordHash")
    role: str = "customer"
    active: bool = True
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str