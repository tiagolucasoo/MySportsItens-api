from fastapi import APIRouter, HTTPException
from api.models.category import Category
from api.database import db

router = APIRouter()

@router.get("/")
async def list_categories():
    categories = await db.categories.find().to_list(length=100)
    
    for category in categories:
        category["_id"] = str(category["_id"])
        
    return categories

@router.post("/")
async def create_category(category: Category):
    new_category = await db.categories.insert_one(category.model_dump(by_alias=True))
    return {"id": str(new_category.inserted_id)}