from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# URI de conexão com seu MongoDB Atlas
uri = "mongodb+srv://pedrohvsalves_db_user:K2bRnodANcEMPxYZ@cluster0.vvfcy0z.mongodb.net/?retryWrites=true&w=majority"

# Criar cliente e conectar ao servidor
client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

# Selecionar o banco de dados
db = client.mercadolivre

# Função para testar a conexão
def test_connection():
    try:
        # Enviar um ping para confirmar conexão
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return False

# Função para obter referência ao banco
def get_database():
    return db
