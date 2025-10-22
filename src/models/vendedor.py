from config import db

"""
Schema da coleção Vendedor
Estrutura: { codVendedor, nome, email }
"""

def create_vendedor_schema(cod_vendedor, nome, email):
    """
    Retorna o schema base para um vendedor
    """
    return {
        "codVendedor": cod_vendedor,  # Código único do vendedor
        "nome": nome,          # Nome completo do vendedor
        "email": email          # Email do vendedor
    }

def validate_vendedor_data(vendedor_data):
    """
    Valida os dados do vendedor antes de inserir/atualizar
    """
    errors = []
    
    if not vendedor_data.get("codVendedor"):
        errors.append("codVendedor é obrigatório")
    
    if not vendedor_data.get("nome"):
        errors.append("nome é obrigatório")
    
    if not vendedor_data.get("email"):
        errors.append("email é obrigatório")
    
    return errors

def format_vendedor_for_display(vendedor):
    """
    Formata o vendedor para exibição
    """
    return f"Vendedor: {vendedor['nome']} (Código: {vendedor['codVendedor']}) - {vendedor['email']}"

def insert_vendedor(vendedor_data):
    """
    Insere um novo vendedor no banco de dados
    """
    errors = validate_vendedor_data(vendedor_data)
    if errors:
        return False, errors
    result = db.vendedor.insert_one(vendedor_data)
    return True, result.inserted_id

def find_vendedor(nome=None):
    """
    Busca vendedores por nome ou retorna todos se nome não for fornecido
    """
    query = {"nome": nome} if nome else {}
    return list(db.vendedor.find(query))

def update_vendedor(cod_vendedor, novos_dados):
    """
    Atualiza um vendedor pelo código
    """
    return db.vendedor.update_one({"codVendedor": cod_vendedor}, {"$set": novos_dados})

def delete_vendedor(cod_vendedor):
    """
    Deleta um vendedor pelo código
    """
    return db.vendedor.delete_one({"codVendedor": cod_vendedor})