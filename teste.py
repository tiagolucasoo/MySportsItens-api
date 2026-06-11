import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega a string direto do seu .env
load_dotenv()
uri = os.getenv("MONGO_URI")

if not uri:
    print("Erro: MONGO_URI não encontrada no .env")
else:
    # O timeout de 5000ms evita que fique travado por 30 segundos
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)

    try:
        print(f"Tentando conectar ao banco usando a rede atual...")
        client.admin.command('ping')
        print("✅ Conexão bem-sucedida! O banco está acessível.")
    except Exception as e:
        print(f"❌ Falha ao conectar. Erro: {e}")