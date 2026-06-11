from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from api.models.user import User, UserCreate, UserLogin
from api.database import db
import uuid

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    hashed_password = pwd_context.hash(user.password)
    unique_code = f"USER-{uuid.uuid4().hex[:6].upper()}"

    new_user = User(
        code=unique_code,
        name=user.name,
        email=user.email,
        passwordHash=hashed_password,
        role="customer"
    )

    result = await db.users.insert_one(new_user.model_dump(by_alias=True, exclude_none=True))
    return {"id": str(result.inserted_id), "code": unique_code, "message": "Usuário criado com sucesso!"}


@router.post("/login")
async def login_user(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    password_matches = pwd_context.verify(credentials.password, user["passwordHash"])
    
    if not password_matches:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    return {
        "message": "Login efetuado com sucesso!",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }