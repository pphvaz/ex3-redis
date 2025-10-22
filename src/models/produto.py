from config import db

"""
Schema da coleção Produto
Estrutura: { codProduto, descricao, preco, estoque }
"""

def create_produto_schema(cod_produto, descricao, preco, estoque):
    """
    Retorna o schema base para um produto
    """
    return {
        "codProduto": cod_produto,    # Código único do produto
        "descricao": descricao,     # Descrição do produto
        "preco": float(preco),        # Preço do produto
        "estoque": int(estoque)         # Quantidade em estoque
    }

def validate_produto_data(produto_data):
    """
    Valida os dados do produto antes de inserir/atualizar
    """
    errors = []
    
    if not produto_data.get("codProduto"):
        errors.append("codProduto é obrigatório")
    
    if not produto_data.get("descricao"):
        errors.append("descricao é obrigatória")
    
    if not isinstance(produto_data.get("preco"), (int, float)) or produto_data.get("preco") < 0:
        errors.append("preco deve ser um número positivo")
    
    if not isinstance(produto_data.get("estoque"), int) or produto_data.get("estoque") < 0:
        errors.append("estoque deve ser um número inteiro positivo")
    
    return errors

def format_produto_for_display(produto):
    """
    Formata o produto para exibição
    """
    return f"Produto: {produto['descricao']} (Código: {produto['codProduto']}) - R$ {produto['preco']:.2f} - Estoque: {produto['estoque']}"

def update_estoque(produto, quantidade):
    """
    Atualiza o estoque do produto
    """
    novo_estoque = produto.get("estoque", 0) + quantidade
    
    if novo_estoque < 0:
        return False, "Estoque não pode ser negativo"
    
    produto["estoque"] = novo_estoque
    return True, f"Estoque atualizado para {novo_estoque}"

def verificar_disponibilidade(produto, quantidade_desejada):
    """
    Verifica se há estoque suficiente para a quantidade desejada
    """
    estoque_atual = produto.get("estoque", 0)
    
    if estoque_atual >= quantidade_desejada:
        return True, f"Produto disponível. Estoque: {estoque_atual}"
    else:
        return False, f"Estoque insuficiente. Disponível: {estoque_atual}, Solicitado: {quantidade_desejada}"

def insert_produto(produto_data):
    """
    Insere um novo produto no banco de dados
    """
    errors = validate_produto_data(produto_data)
    if errors:
        return False, errors
    result = db.produto.insert_one(produto_data)
    return True, result.inserted_id

def find_produto(descricao=None):
    """
    Busca produtos por descrição ou retorna todos se descrição não for fornecida
    """
    query = {"descricao": {"$regex": descricao, "$options": "i"}} if descricao else {}
    return list(db.produto.find(query))

def update_produto(cod_produto, novos_dados):
    """
    Atualiza um produto pelo código
    """
    return db.produto.update_one({"codProduto": cod_produto}, {"$set": novos_dados})

def delete_produto(cod_produto):
    """
    Deleta um produto pelo código
    """
    return db.produto.delete_one({"codProduto": cod_produto})
