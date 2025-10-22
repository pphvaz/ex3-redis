"""
Schema da coleção Compra
Estrutura: { data, precoTotal, usuario: {usuarioId, nome, email}, vendedor: {codVendedor}, itens: [Produto] }
"""

from datetime import datetime
from config import db

def create_compra_schema():
    """
    Retorna o schema base para uma compra
    """
    return {
        "data": "",                # Data da compra
        "precoTotal": 0.0,        # Preço total da compra
        "usuario": {               # Dados do usuário (documento aninhado)
            "usuarioId": "",
            "nome": "",
            "email": ""
        },
        "vendedor": {              # Dados do vendedor (documento aninhado)
            "codVendedor": ""
        },
        "itens": []                # Lista de produtos comprados (documentos aninhados)
    }

def create_item_compra_schema():
    """
    Retorna o schema para um item de compra (documento aninhado)
    """
    return {
        "codProduto": "",          # Código do produto
        "descricao": "",           # Descrição do produto
        "preco": 0.0,              # Preço unitário do produto
        "quantidade": 1,           # Quantidade comprada
        "subtotal": 0.0            # Preço total do item (preco * quantidade)
    }

def validate_compra_data(compra_data):
    """
    Valida os dados da compra antes de inserir/atualizar
    """
    errors = []
    
    if not compra_data.get("data"):
        errors.append("data é obrigatória")
    
    if not isinstance(compra_data.get("precoTotal"), (int, float)) or compra_data.get("precoTotal") <= 0:
        errors.append("precoTotal deve ser um número positivo")
    
    if not compra_data.get("usuario") or not compra_data["usuario"].get("usuarioId"):
        errors.append("dados do usuário são obrigatórios")
    
    if not compra_data.get("vendedor") or not compra_data["vendedor"].get("codVendedor"):
        errors.append("dados do vendedor são obrigatórios")
    
    if not compra_data.get("itens") or len(compra_data["itens"]) == 0:
        errors.append("a compra deve ter pelo menos um item")
    
    return errors

def format_compra_for_display(compra):
    """
    Formata a compra para exibição
    """
    return f"Compra em {compra['data']} - Total: R$ {compra['precoTotal']:.2f} - Usuário: {compra['usuario']['nome']}"

def calcular_preco_total(itens):
    """
    Calcula o preço total da compra baseado nos itens
    """
    total = 0.0
    for item in itens:
        subtotal = item.get("preco", 0) * item.get("quantidade", 1)
        item["subtotal"] = subtotal
        total += subtotal
    
    return total

def adicionar_item_compra(compra, produto, quantidade=1):
    """
    Adiciona um item à compra
    """
    if "itens" not in compra:
        compra["itens"] = []
    
    # Verificar se o produto já está na compra
    for item in compra["itens"]:
        if item["codProduto"] == produto["codProduto"]:
            # Atualizar quantidade e subtotal
            item["quantidade"] += quantidade
            item["subtotal"] = item["preco"] * item["quantidade"]
            return True, "Quantidade do item atualizada"
    
    # Criar novo item
    novo_item = {
        "codProduto": produto["codProduto"],
        "descricao": produto["descricao"],
        "preco": produto["preco"],
        "quantidade": quantidade,
        "subtotal": produto["preco"] * quantidade
    }
    
    compra["itens"].append(novo_item)
    return True, "Item adicionado à compra"

def finalizar_compra(compra):
    """
    Finaliza a compra, calculando o total e definindo a data
    """
    # Definir data atual
    compra["data"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Calcular preço total
    compra["precoTotal"] = calcular_preco_total(compra["itens"])
    
    return True, "Compra finalizada com sucesso"

def insert_compra(compra_data):
    """
    Insere uma nova compra no banco de dados
    """
    errors = validate_compra_data(compra_data)
    if errors:
        return False, errors
    result = db.compra.insert_one(compra_data)
    return True, result.inserted_id

def find_compra(usuario_nome=None, data_inicio=None, data_fim=None):
    """
    Busca compras por usuário, data ou retorna todas se nenhum filtro for fornecido
    """
    query = {}
    
    if usuario_nome:
        query["usuario.nome"] = {"$regex": usuario_nome, "$options": "i"}
    
    if data_inicio and data_fim:
        # Para busca por data, assumindo formato DD/MM/YYYY
        query["data"] = {"$gte": data_inicio, "$lte": data_fim}
    elif data_inicio:
        query["data"] = {"$gte": data_inicio}
    elif data_fim:
        query["data"] = {"$lte": data_fim}
    
    return list(db.compra.find(query).sort("data", -1))

def update_compra(compra_id, novos_dados):
    """
    Atualiza uma compra pelo ID
    """
    return db.compra.update_one({"_id": compra_id}, {"$set": novos_dados})

def delete_compra(compra_id):
    """
    Deleta uma compra pelo ID e remove do histórico do usuário
    """
    # Primeiro, buscar a compra para obter informações do usuário
    compra_encontrada = db.compra.find_one({"_id": compra_id})
    
    if compra_encontrada:
        # Remover a compra do histórico do usuário
        usuario_nome = compra_encontrada.get("usuario", {}).get("nome")
        if usuario_nome:
            # Remover a compra específica do array comprasEfetuadas do usuário
            # Usando a data como identificador único da compra no histórico
            db.usuario.update_one(
                {"nome": usuario_nome},
                {"$pull": {"comprasEfetuadas": {"data": compra_encontrada.get("data")}}}
            )
    
    # Deletar a compra da coleção principal
    return db.compra.delete_one({"_id": compra_id})

def add_compra_to_usuario(usuario_nome, compra_data):
    """
    Adiciona uma compra ao histórico do usuário
    """
    # Buscar o usuário
    usuarios = db.usuario.find({"nome": usuario_nome})
    usuario = usuarios[0] if usuarios else None
    
    if not usuario:
        return False, "Usuário não encontrado"
    
    # Adicionar compra ao histórico
    if "comprasEfetuadas" not in usuario:
        usuario["comprasEfetuadas"] = []
    
    # Criar uma versão simplificada da compra para o histórico do usuário
    compra_historico = {
        "data": compra_data["data"],
        "precoTotal": compra_data["precoTotal"],
        "vendedor": compra_data["vendedor"]["codVendedor"],
        "itens": compra_data["itens"]
    }
    
    usuario["comprasEfetuadas"].append(compra_historico)
    
    # Atualizar o usuário no banco
    result = db.usuario.update_one(
        {"_id": usuario["_id"]}, 
        {"$set": {"comprasEfetuadas": usuario["comprasEfetuadas"]}}
    )
    
    if result.modified_count > 0:
        return True, "Compra adicionada ao histórico do usuário"
    else:
        return False, "Erro ao atualizar histórico do usuário"
