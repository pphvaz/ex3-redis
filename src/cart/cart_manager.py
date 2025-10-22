
import json
from datetime import datetime
from ..models import produto
from ..myredis import redis_manager

class CartManager:
    def __init__(self):
        self.redis = redis_manager
    
    def add_to_cart(self, user_id, cod_produto, quantity=1):
        """
        Add product to user's cart
        Returns (success, message)
        """
        try:
            # Find product in database
            produtos = produto.find_produto()
            produto_encontrado = None
            for prod in produtos:
                if prod.get('codProduto') == cod_produto:
                    produto_encontrado = prod
                    break
            
            if not produto_encontrado:
                return False, "Produto não encontrado"
            
            # Check availability
            disponivel, msg = produto.verificar_disponibilidade(produto_encontrado, quantity)
            if not disponivel:
                return False, f"Produto não disponível: {msg}"
            
            # Add to cart
            product_data = {
                "codProduto": produto_encontrado.get('codProduto'),
                "descricao": produto_encontrado.get('descricao'),
                "preco": produto_encontrado.get('preco')
            }
            
            success, message = self.redis.add_item_to_cart(user_id, product_data, quantity)
            if success:
                return True, f"Produto '{produto_encontrado.get('descricao')}' adicionado ao carrinho!"
            else:
                return False, f"Erro ao adicionar ao carrinho: {message}"
                
        except Exception as e:
            return False, f"Erro ao adicionar ao carrinho: {str(e)}"
    
    def remove_from_cart(self, user_id, cod_produto):
        """
        Remove product from user's cart
        Returns (success, message)
        """
        try:
            success, message = self.redis.remove_item_from_cart(user_id, cod_produto)
            if success:
                return True, "Produto removido do carrinho!"
            else:
                return False, f"Erro ao remover do carrinho: {message}"
        except Exception as e:
            return False, f"Erro ao remover do carrinho: {str(e)}"
    
    def get_cart(self, user_id):
        """
        Get user's cart
        Returns (success, message, cart_data)
        """
        try:
            success, cart_data = self.redis.get_user_cart(user_id)
            if success:
                return True, "Carrinho obtido com sucesso", cart_data
            else:
                return False, f"Erro ao obter carrinho: {cart_data}", None
        except Exception as e:
            return False, f"Erro ao obter carrinho: {str(e)}", None
    
    def get_cart_summary(self, user_id):
        """
        Get cart summary
        Returns (success, message, summary)
        """
        try:
            success, summary = self.redis.get_cart_summary(user_id)
            if success:
                return True, "Resumo do carrinho obtido", summary
            else:
                return False, f"Erro ao obter resumo: {summary}", None
        except Exception as e:
            return False, f"Erro ao obter resumo: {str(e)}", None
    
    def clear_cart(self, user_id):
        """
        Clear user's cart
        Returns (success, message)
        """
        try:
            success, message = self.redis.clear_user_cart(user_id)
            if success:
                return True, "Carrinho limpo com sucesso!"
            else:
                return False, f"Erro ao limpar carrinho: {message}"
        except Exception as e:
            return False, f"Erro ao limpar carrinho: {str(e)}"
    
    def display_cart(self, user_id):
        """
        Display user's cart in a formatted way
        Returns (success, message, display_text)
        """
        try:
            success, message, cart_data = self.get_cart(user_id)
            if not success:
                return False, message, None
            
            items = cart_data.get('items', [])
            total = cart_data.get('total', 0)
            
            if not items:
                return True, "Carrinho vazio", "🛒 Seu carrinho está vazio"
            
            display = "🛒 SEU CARRINHO\n"
            display += "=" * 50 + "\n"
            
            for i, item in enumerate(items, 1):
                display += f"{i}. {item.get('descricao', 'N/A')}\n"
                display += f"   Código: {item.get('codProduto', 'N/A')}\n"
                display += f"   Preço: R$ {item.get('preco', 0):.2f}\n"
                display += f"   Quantidade: {item.get('quantidade', 0)}\n"
                display += f"   Subtotal: R$ {item.get('subtotal', 0):.2f}\n"
                display += "-" * 30 + "\n"
            
            display += f"TOTAL: R$ {total:.2f}\n"
            display += "=" * 50
            
            return True, "Carrinho exibido", display
            
        except Exception as e:
            return False, f"Erro ao exibir carrinho: {str(e)}", None
    
    def update_item_quantity(self, user_id, cod_produto, new_quantity):
        """
        Update item quantity in cart
        Returns (success, message)
        """
        try:
            # Get current cart
            success, cart_data = self.get_cart(user_id)
            if not success:
                return False, cart_data
            
            items = cart_data.get('items', [])
            
            # Find and update item
            item_found = False
            for item in items:
                if item.get('codProduto') == cod_produto:
                    if new_quantity <= 0:
                        # Remove item if quantity is 0 or negative
                        items.remove(item)
                    else:
                        # Update quantity
                        item['quantidade'] = new_quantity
                        item['subtotal'] = item['preco'] * new_quantity
                    item_found = True
                    break
            
            if not item_found:
                return False, "Produto não encontrado no carrinho"
            
            # Calculate new total
            total = sum(item.get('subtotal', 0) for item in items)
            
            # Save updated cart
            updated_cart = {
                "items": items,
                "total": total
            }
            
            success, message = self.redis.save_user_cart(user_id, updated_cart)
            if success:
                return True, "Quantidade atualizada com sucesso!"
            else:
                return False, f"Erro ao atualizar quantidade: {message}"
                
        except Exception as e:
            return False, f"Erro ao atualizar quantidade: {str(e)}"
    
    def get_cart_item_count(self, user_id):
        """
        Get total number of items in cart
        Returns (success, count)
        """
        try:
            success, summary = self.get_cart_summary(user_id)
            if success:
                return True, summary.get('total_items', 0)
            else:
                return False, 0
        except Exception as e:
            return False, 0

# Create global cart manager instance
cart_manager = CartManager()
