from config import db

"""
Schema da coleção Usuario
Estrutura: { usuarioId, nome, email, favoritos: [Produto], comprasEfetuadas: [Compra] }
"""

def create_usuario_schema(nome, sobrenome, cpf, enderecos):
    return {
        "nome": nome,
        "sobrenome": sobrenome,
        "cpf": cpf,
        "end": enderecos
    }

def validate_usuario(usuario):
    errors = []
    if not usuario.get("nome"):
        errors.append("Nome é obrigatório")
    if not usuario.get("cpf"):
        errors.append("CPF é obrigatório")
    return errors

def insert_usuario(usuario_data):
    errors = validate_usuario(usuario_data)
    if errors:
        return False, errors
    result = db.usuario.insert_one(usuario_data)
    return True, result.inserted_id

def find_usuario(nome=None):
    query = {"nome": nome} if nome else {}
    return list(db.usuario.find(query))

def update_usuario(nome, novos_dados):
    return db.usuario.update_one({"nome": nome}, {"$set": novos_dados})

def delete_usuario(nome, sobrenome):
    return db.usuario.delete_one({"nome": nome, "sobrenome": sobrenome})

def create_produto_favorito_schema(codProduto, descricao, preco):
    """
    Retorna o schema para um produto favorito (documento aninhado)
    """
    return {
        "codProduto": codProduto,          # Código do produto
        "descricao": descricao,           # Descrição do produto
        "preco": preco,              # Preço do produto
    }

def format_usuario_for_display(usuario):
    """
    Formata o usuário para exibição
    """
    return f"Usuário: {usuario['nome']} (ID: {usuario['usuarioId']}) - {usuario['email']}"

def add_produto_favorito(usuario, produto):
    """
    Adiciona um produto aos favoritos do usuário
    """
    if "favoritos" not in usuario:
        usuario["favoritos"] = []
    
    # Verificar se o produto já não está nos favoritos
    for favorito in usuario["favoritos"]:
        if favorito["codProduto"] == produto["codProduto"]:
            return False, "Produto já está nos favoritos"
    
    usuario["favoritos"].append(produto)
    return True, "Produto adicionado aos favoritos"

def add_compra(usuario, compra):
    """
    Adiciona uma compra ao histórico do usuário
    """
    if "comprasEfetuadas" not in usuario:
        usuario["comprasEfetuadas"] = []
    
    usuario["comprasEfetuadas"].append(compra)
    return True, "Compra adicionada ao histórico"