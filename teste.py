import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")

if not uri:
    print("Erro: MONGO_URI não encontrada no .env")
else:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)

    try:
        print(f"Tentando conectar ao banco usando a rede atual...")
        client.admin.command('ping')
        print("✅ Conexão bem-sucedida! O banco está acessível.")
    except Exception as e:
        print(f"❌ Falha ao conectar. Erro: {e}")