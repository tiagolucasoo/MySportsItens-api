from fastapi import APIRouter, HTTPException, Depends
from api.services.auth import admin_only, all_users
from api.models.category import Category
from api.database import db

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/")
async def list_categories():
    categories = await db.categories.find().to_list(length=100)
    
    for category in categories:
        category["_id"] = str(category["_id"])
        
    return categories

@router.post("/")
async def create_category(category: Category, user = Depends(admin_only)):
    new_category = await db.categories.insert_one(category.model_dump(by_alias=True))
    return {"id": str(new_category.inserted_id)}