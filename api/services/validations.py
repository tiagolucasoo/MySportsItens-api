from fastapi import HTTPException
from pydantic import EmailStr, ValidationError
from api.database import db

def email(email: str):
    try:
        EmailStr(email)
    except ValidationError:
        raise HTTPException(status_code=400, detail="E-mail inválido.")

async def email_exists(email: str):
    user = await db.users.find_one({"email": email})

    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")