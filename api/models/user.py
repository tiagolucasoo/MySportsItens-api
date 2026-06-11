from fastapi import APIRouter, HTTPException, status
import bcrypt
import uuid
from api.models.user import User, UserCreate, UserLogin
from api.database import db

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt).decode('utf-8')

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

    password_matches = bcrypt.checkpw(
        credentials.password.encode('utf-8'), 
        user["passwordHash"].encode('utf-8')
    )
    
    if not password_matches:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    return {
        "message": "Login efetuado com sucesso!",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "customer")
        }
    }