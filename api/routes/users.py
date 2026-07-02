from fastapi import APIRouter, HTTPException, status
import uuid

from api.database import db
from api.models.user import User, UserCreate, UserLogin
from api.services.auth import (hash_password, check_password, create_token)
from api.services.validations import (email_exists)

router = APIRouter(tags=["Users"], prefix="/users")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    await email_exists(user.email)

    code = f"USER-{uuid.uuid4().hex[:6].upper()}"

    new_user = User(
                    code=code,
                    name=user.name,
                    email=user.email,
                    passwordHash=hash_password(user.password),
                    role="customer")

    result = await db.users.insert_one(new_user.model_dump(by_alias=True, exclude_none=True))

    return {
        "id": str(result.inserted_id),
        "code": code,
        "message": "Usuário criado com sucesso!"
    }

@router.post("/login")
async def login_user(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email})

    if not user or not check_password(credentials.password, user["passwordHash"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = create_token({
        "sub": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role", "customer")
    })

    return {
        "message": "Login efetuado com sucesso!",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "customer")
        }
    }