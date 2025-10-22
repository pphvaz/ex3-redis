from pymongo import MongoClient
import certifi

# URI direto do Atlas (copiar do dashboard)
MONGO_URI = "mongodb+srv://pedroalves01_db_user:q6GZrcJa5UIwnwuQ@gsw.fv9pu92.mongodb.net/?retryWrites=true&w=majority&appName=gsw"

# Nome do banco
DB_NAME = "mercadolivre"

# Cria cliente Mongo e exporta a referência do db
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]