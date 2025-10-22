from pymongo import MongoClient
import certifi
import redis

# URI direto do Atlas (copiar do dashboard)
MONGO_URI = "mongodb+srv://pedroalves01_db_user:q6GZrcJa5UIwnwuQ@gsw.fv9pu92.mongodb.net/?retryWrites=true&w=majority&appName=gsw"

# Nome do banco
DB_NAME = "mercadolivre"

# Cria cliente Mongo e exporta a referência do db
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]

# Redis Configuration
REDIS_HOST = "redis-17140.c283.us-east-1-4.ec2.redns.redis-cloud.com"
REDIS_PORT = 17140
REDIS_USERNAME = "default"
REDIS_PASSWORD = "zH4Q0dGD59UWxxP7zv5hODcZz05wo0ML"

# Cria cliente Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    decode_responses=True
)