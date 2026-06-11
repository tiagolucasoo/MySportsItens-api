from fastapi import APIRouter, HTTPException, status
import hashlib
import os
import uuid
import jwt
from datetime import datetime, timedelta
from api.models.user import User, UserCreate, UserLogin
from api.database import db

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"{salt.hex()}:{pwd_hash.hex()}"

def verify_password(plain_password: str, stored_password_hash: str) -> bool:
    try:
        salt_hex, pwd_hash_hex = stored_password_hash.split(':')
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(pwd_hash_hex)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return pwd_hash == expected_hash
    except ValueError:
        return False

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    hashed_password = hash_password(user.password)
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

    if not verify_password(credentials.password, user["passwordHash"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token_payload = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "role": user.get("role", "customer")
    }
    
    token = create_access_token(token_payload)

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