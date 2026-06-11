import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("Variável do Mongo não configurada")

client = AsyncIOMotorClient(MONGO_URI)
db = client.MySportItens