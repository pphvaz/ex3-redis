"""
Enhanced Menu System with Redis Authentication and Cart Management
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .models import usuario, vendedor, produto, compra
from .config import client, db
from .auth.auth import auth_manager
from .cart.cart_manager import cart_manager
from .myredis import redis_manager

class EnhancedMenu:
    def __init__(self):
        self.current_user_id = None
        self.current_user_data = None
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("           SISTEMA MERCADO LIVRE - ENHANCED")
        print("           Com Autenticação e Carrinho Redis")
        print("="*60)
    
    def display_user_status(self):
        """Display current user status"""
        if self.current_user_id and self.current_user_data:
            user_name = auth_manager.get_user_display_name(self.current_user_data)
            success, count = cart_manager.get_cart_item_count(self.current_user_id)
            cart_count = count if success else 0
            print(f"👤 Usuário: {user_name}")
            print(f"🛒 Itens no carrinho: {cart_count}")
        else:
            print("👤 Usuário: Não logado")
    
    def login_menu(self):
        """Handle user login"""
        print("\n" + "="*40)
        print("           LOGIN")
        print("="*40)
        
        nome = input("Digite seu nome: ").strip()
        if not nome:
            print("Nome é obrigatório!")
            return False
        
        cpf = input("Digite seu CPF (opcional): ").strip()
        cpf = cpf if cpf else None
        
        success, message, user_data = auth_manager.login_user(nome, cpf)
        print(f"\n{message}")
        
        if success:
            self.current_user_id = user_data.get('mongo_id')
            self.current_user_data = user_data
            
            # Load existing cart if any
            success_cart, message_cart, cart_data = cart_manager.get_cart(self.current_user_id)
            if success_cart and cart_data and cart_data.get('items'):
                print(f"🛒 Carrinho carregado com {len(cart_data.get('items', []))} item(s)")
            
            return True
        else:
            return False
    
    def logout_user(self):
        """Handle user logout"""
        if self.current_user_id:
            success, message = auth_manager.logout_user(self.current_user_id)
            print(f"\n{message}")
            self.current_user_id = None
            self.current_user_data = None
        else:
            print("Nenhum usuário logado.")
    
    def cart_menu(self):
        """Handle cart operations"""
        if not self.current_user_id:
            print("Você precisa estar logado para acessar o carrinho!")
            return
        
        while True:
            print("\n" + "="*40)
            print("           CARRINHO DE COMPRAS")
            print("="*40)
            print("1 - Ver carrinho")
            print("2 - Adicionar produto")
            print("3 - Remover produto")
            print("4 - Atualizar quantidade")
            print("5 - Limpar carrinho")
            print("V - Voltar")
            print("="*40)
            
            choice = input("Digite a opção desejada: ").strip().upper()
            
            if choice == '1':
                self.view_cart()
            elif choice == '2':
                self.add_to_cart()
            elif choice == '3':
                self.remove_from_cart()
            elif choice == '4':
                self.update_cart_quantity()
            elif choice == '5':
                self.clear_cart()
            elif choice == 'V':
                break
            else:
                print("Opção inválida!")
    
    def view_cart(self):
        """View current cart"""
        success, message, display_text = cart_manager.display_cart(self.current_user_id)
        if success:
            print(f"\n{display_text}")
        else:
            print(f"Erro: {message}")
    
    def add_to_cart(self):
        """Add product to cart"""
        print("\n=== ADICIONAR PRODUTO AO CARRINHO ===")
        
        # Show available products
        produtos = produto.find_produto()
        if not produtos:
            print("Nenhum produto disponível.")
            return
        
        print("\nPRODUTOS DISPONÍVEIS:")
        print("-" * 50)
        for prod in produtos:
            estoque = prod.get('estoque', 0)
            status = "✅ Disponível" if estoque > 0 else "❌ Sem estoque"
            print(f"Código: {prod.get('codProduto', 'N/A')}")
            print(f"  Descrição: {prod.get('descricao', 'N/A')}")
            print(f"  Preço: R$ {prod.get('preco', 0):.2f}")
            print(f"  Estoque: {estoque} - {status}")
            print("-" * 30)
        
        cod_produto = input("\nDigite o código do produto: ").strip()
        if not cod_produto:
            print("Código do produto é obrigatório!")
            return
        
        try:
            quantidade = int(input("Digite a quantidade: "))
            if quantidade <= 0:
                print("Quantidade deve ser positiva!")
                return
        except ValueError:
            print("Quantidade deve ser um número!")
            return
        
        success, message = cart_manager.add_to_cart(self.current_user_id, cod_produto, quantidade)
        print(f"\n{message}")
    
    def remove_from_cart(self):
        """Remove product from cart"""
        print("\n=== REMOVER PRODUTO DO CARRINHO ===")
        
        # Show current cart
        success, message, display_text = cart_manager.display_cart(self.current_user_id)
        if not success:
            print(f"Erro: {message}")
            return
        
        print(f"\n{display_text}")
        
        cod_produto = input("\nDigite o código do produto a remover: ").strip()
        if not cod_produto:
            print("Código do produto é obrigatório!")
            return
        
        success, message = cart_manager.remove_from_cart(self.current_user_id, cod_produto)
        print(f"\n{message}")
    
    def update_cart_quantity(self):
        """Update product quantity in cart"""
        print("\n=== ATUALIZAR QUANTIDADE ===")
        
        # Show current cart
        success, message, display_text = cart_manager.display_cart(self.current_user_id)
        if not success:
            print(f"Erro: {message}")
            return
        
        print(f"\n{display_text}")
        
        cod_produto = input("\nDigite o código do produto: ").strip()
        if not cod_produto:
            print("Código do produto é obrigatório!")
            return
        
        try:
            nova_quantidade = int(input("Digite a nova quantidade: "))
        except ValueError:
            print("Quantidade deve ser um número!")
            return
        
        success, message = cart_manager.update_item_quantity(self.current_user_id, cod_produto, nova_quantidade)
        print(f"\n{message}")
    
    def clear_cart(self):
        """Clear entire cart"""
        confirmacao = input("Tem certeza que deseja limpar o carrinho? (s/N): ")
        if confirmacao.lower() in ['s', 'sim', 'y', 'yes']:
            success, message = cart_manager.clear_cart(self.current_user_id)
            print(f"\n{message}")
        else:
            print("Operação cancelada.")
    
    def checkout_menu(self):
        """Handle checkout process"""
        if not self.current_user_id:
            print("Você precisa estar logado para finalizar a compra!")
            return
        
        print("\n" + "="*40)
        print("           FINALIZAR COMPRA")
        print("="*40)
        
        # Show current cart
        success, message, display_text = cart_manager.display_cart(self.current_user_id)
        if not success:
            print(f"Erro: {message}")
            return
        
        print(f"\n{display_text}")
        
        success_cart, message_cart, cart_data = cart_manager.get_cart(self.current_user_id)
        if not success_cart or not cart_data or not cart_data.get('items'):
            print("Carrinho vazio! Adicione produtos antes de finalizar a compra.")
            return
        
        confirmacao = input("\nDeseja finalizar a compra? (s/N): ")
        if confirmacao.lower() not in ['s', 'sim', 'y', 'yes']:
            print("Compra cancelada.")
            return
        
        # Get vendedor
        cod_vendedor = input("Digite o código do vendedor: ").strip()
        vendedores = vendedor.find_vendedor()
        vendedor_compra = None
        for vend in vendedores:
            if vend.get('codVendedor') == cod_vendedor:
                vendedor_compra = vend
                break
        
        if not vendedor_compra:
            print("Vendedor não encontrado.")
            return
        
        # Create purchase data
        from datetime import datetime
        compra_data = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "vendedor": {
                "codVendedor": vendedor_compra.get('codVendedor', ''),
                "nome": vendedor_compra.get('nome', '')
            },
            "itens": cart_data.get('items', []),
            "precoTotal": cart_data.get('total', 0)
        }
        
        # Add purchase to user history
        self.add_purchase_to_user_history(compra_data)
        
        print(f"✅ Compra finalizada com sucesso!")
        print(f"💰 Total: R$ {compra_data['precoTotal']:.2f}")
        print(f"📅 Data: {compra_data['data']}")
        print(f"🏪 Vendedor: {vendedor_compra.get('nome', 'N/A')}")
        
        # Clear cart after successful purchase
        cart_manager.clear_cart(self.current_user_id)
        print("🛒 Carrinho limpo após a compra.")
        print("📋 Compra adicionada ao seu histórico!")
    
    def add_purchase_to_user_history(self, compra_data):
        """Add purchase to user's history in MongoDB"""
        try:
            from config import db
            from bson import ObjectId
            
            # Convert string ID to ObjectId
            user_object_id = ObjectId(self.current_user_id)
            
            # Get current user from MongoDB
            user_doc = db.usuario.find_one({"_id": user_object_id})
            if not user_doc:
                print("Usuário não encontrado no banco de dados.")
                return False
            
            # Initialize comprasHistorico if it doesn't exist
            if "comprasHistorico" not in user_doc:
                user_doc["comprasHistorico"] = []
            
            # Add new purchase to history
            user_doc["comprasHistorico"].append(compra_data)
            
            # Update user document
            result = db.usuario.update_one(
                {"_id": user_object_id},
                {"$set": {"comprasHistorico": user_doc["comprasHistorico"]}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            print(f"Erro ao adicionar compra ao histórico: {e}")
            return False
    
    def main_menu(self):
        """Main application menu"""
        while True:
            self.display_welcome()
            self.display_user_status()
            
            print("\n" + "="*50)
            print("OPÇÕES PRINCIPAIS:")
            print("="*50)
            
            if not self.current_user_id:
                print("1 - Fazer Login")
                print("S - Sair")
            else:
                print("1 - CRUD Usuário")
                print("2 - CRUD Vendedor") 
                print("3 - CRUD Produto")
                print("4 - 🛒 Carrinho de Compras")
                print("5 - 💳 Finalizar Compra")
                print("6 - Logout")
                print("S - Sair")
            
            print("="*50)
            
            choice = input("Digite a opção desejada: ").strip()
            
            if not self.current_user_id:
                if choice == '1':
                    self.login_menu()
                elif choice.upper() == 'S':
                    print("\nObrigado por usar o Sistema Mercado Livre!")
                    break
                else:
                    print("Opção inválida! Faça login primeiro.")
            else:
                if choice == '1':
                    self.user_crud_menu()
                elif choice == '2':
                    self.vendor_crud_menu()
                elif choice == '3':
                    self.product_crud_menu()
                elif choice == '4':
                    self.cart_menu()
                elif choice == '5':
                    self.checkout_menu()
                elif choice == '6':
                    self.logout_user()
                elif choice.upper() == 'S':
                    self.logout_user()
                    print("\nObrigado por usar o Sistema Mercado Livre!")
                    break
                else:
                    print("Opção inválida!")
    
    def user_crud_menu(self):
        """User CRUD operations"""
        while True:
            print("\n" + "="*30)
            print("      MENU USUÁRIO")
            print("="*30)
            print("1 - Create Usuário")
            print("2 - Read Usuário")
            print("3 - Update Usuário")
            print("4 - Delete Usuário")
            print("V - Voltar")
            print("="*30)
            sub = input("Digite a opção desejada: ")

            if (sub == '1'):
                print("=== CREATE USUÁRIO ===")
                nome = input("Digite o nome: ")
                sobrenome = input("Digite o sobrenome: ")
                cpf = input("Digite o CPF: ")
                enderecos = input("Digite os endereços (separados por vírgula): ").split(',')
                enderecos = [end.strip() for end in enderecos if end.strip()]
                
                usuario_data = usuario.create_usuario_schema(nome, sobrenome, cpf, enderecos)
                success, result = usuario.insert_usuario(usuario_data)
                
                if success:
                    print(f"Usuário criado com sucesso! ID: {result}")
                else:
                    print(f"Erro ao criar usuário: {result}")
                
            elif (sub == '2'):
                print("=== READ USUÁRIO ===")
                nome = input("Digite o nome do usuário (ou deixe vazio para listar todos): ")
                usuarios = usuario.find_usuario(nome if nome else None)
                
                if usuarios:
                    print(f"\nEncontrados {len(usuarios)} usuário(s):")
                    for user in usuarios:
                        print(f"- Nome: {user.get('nome', 'N/A')} {user.get('sobrenome', 'N/A')}")
                        print(f"  CPF: {user.get('cpf', 'N/A')}")
                        enderecos = user.get('end', [])
                        if enderecos:
                            if isinstance(enderecos[0], str):
                                print(f"  Endereços: {', '.join(enderecos)}")
                            else:
                                enderecos_str = [str(end) for end in enderecos]
                                print(f"  Endereços: {', '.join(enderecos_str)}")
                        else:
                            print(f"  Endereços: Nenhum")
                        
                        # Show purchase history
                        compras_historico = user.get('comprasHistorico', [])
                        if compras_historico:
                            print(f"  📋 Histórico de Compras ({len(compras_historico)} compra(s)):")
                            for i, compra in enumerate(compras_historico, 1):
                                print(f"    {i}. Data: {compra.get('data', 'N/A')}")
                                print(f"       Vendedor: {compra.get('vendedor', {}).get('nome', 'N/A')}")
                                print(f"       Total: R$ {compra.get('precoTotal', 0):.2f}")
                                print(f"       Itens: {len(compra.get('itens', []))} produto(s)")
                        else:
                            print(f"  📋 Histórico de Compras: Nenhuma compra realizada")
                        
                        print(f"  ID: {user.get('_id', 'N/A')}")
                        print()
                else:
                    print("Nenhum usuário encontrado.")
            
            elif (sub == '3'):
                print("=== UPDATE USUÁRIO ===")
                nome = input("Digite o nome do usuário a ser atualizado: ")
                
                usuarios = usuario.find_usuario(nome)
                if not usuarios:
                    print("Usuário não encontrado.")
                    continue
                
                user = usuarios[0]
                print(f"\nDados atuais do usuário {user.get('nome', 'N/A')}:")
                print(f"CPF: {user.get('cpf', 'N/A')}")
                enderecos = user.get('end', [])
                if enderecos:
                    if isinstance(enderecos[0], str):
                        print(f"Endereços: {', '.join(enderecos)}")
                    else:
                        enderecos_str = [str(end) for end in enderecos]
                        print(f"Endereços: {', '.join(enderecos_str)}")
                else:
                    print("Endereços: Nenhum")
                
                print("\nDigite os novos dados (deixe vazio para manter o atual):")
                novo_sobrenome = input(f"Novo sobrenome (atual: {user.get('sobrenome', 'N/A')}): ")
                novo_cpf = input(f"Novo CPF (atual: {user.get('cpf', 'N/A')}): ")
                
                enderecos_atuais = user.get('end', [])
                if enderecos_atuais:
                    if isinstance(enderecos_atuais[0], str):
                        enderecos_str = ', '.join(enderecos_atuais)
                    else:
                        enderecos_str = ', '.join([str(end) for end in enderecos_atuais])
                else:
                    enderecos_str = "Nenhum"
                
                novos_enderecos = input(f"Novos endereços (atual: {enderecos_str}): ")
                
                novos_dados = {}
                if novo_sobrenome:
                    novos_dados['sobrenome'] = novo_sobrenome
                if novo_cpf:
                    novos_dados['cpf'] = novo_cpf
                if novos_enderecos:
                    novos_dados['end'] = [end.strip() for end in novos_enderecos.split(',') if end.strip()]
                
                if novos_dados:
                    result = usuario.update_usuario(nome, novos_dados)
                    if result.modified_count > 0:
                        print("Usuário atualizado com sucesso!")
                    else:
                        print("Nenhuma alteração foi feita.")
                else:
                    print("Nenhuma alteração foi fornecida.")

            elif (sub == '4'):
                print("=== DELETE USUÁRIO ===")
                nome = input("Digite o nome do usuário a ser deletado: ")
                sobrenome = input("Digite o sobrenome do usuário a ser deletado: ")
                
                confirmacao = input(f"Tem certeza que deseja deletar {nome} {sobrenome}? (s/N): ")
                if confirmacao.lower() in ['s', 'sim', 'y', 'yes']:
                    result = usuario.delete_usuario(nome, sobrenome)
                    if result.deleted_count > 0:
                        print("Usuário deletado com sucesso!")
                    else:
                        print("Usuário não encontrado ou não foi deletado.")
                else:
                    print("Operação cancelada.")
            
            elif (sub.lower() == 'v'):
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida!")
    
    def vendor_crud_menu(self):
        """Vendor CRUD operations"""
        while True:
            print("\n" + "="*30)
            print("      MENU VENDEDOR")
            print("="*30)
            print("1 - Create Vendedor")
            print("2 - Read Vendedor")
            print("3 - Update Vendedor")
            print("4 - Delete Vendedor")
            print("V - Voltar")
            print("="*30)
            sub = input("Digite a opção desejada: ")
            
            if (sub == '1'):
                print("=== CREATE VENDEDOR ===")
                cod_vendedor = input("Digite o código do vendedor: ")
                nome = input("Digite o nome: ")
                email = input("Digite o email: ")
                
                vendedor_data = vendedor.create_vendedor_schema(cod_vendedor, nome, email)
                success, result = vendedor.insert_vendedor(vendedor_data)
                
                if success:
                    print(f"Vendedor criado com sucesso! ID: {result}")
                else:
                    print(f"Erro ao criar vendedor: {result}")
            
            elif (sub == '2'):
                print("=== READ VENDEDOR ===")
                nome = input("Digite o nome do vendedor (ou deixe vazio para listar todos): ")
                vendedores = vendedor.find_vendedor(nome if nome else None)
                
                if vendedores:
                    print(f"\nEncontrados {len(vendedores)} vendedor(es):")
                    for vend in vendedores:
                        print(f"- Nome: {vend.get('nome', 'N/A')}")
                        print(f"  Código: {vend.get('codVendedor', 'N/A')}")
                        print(f"  Email: {vend.get('email', 'N/A')}")
                        print(f"  ID: {vend.get('_id', 'N/A')}")
                        print()
                else:
                    print("Nenhum vendedor encontrado.")
            
            elif (sub == '3'):
                print("=== UPDATE VENDEDOR ===")
                cod_vendedor = input("Digite o código do vendedor a ser atualizado: ")
                
                vendedores = vendedor.find_vendedor()
                vendedor_encontrado = None
                for vend in vendedores:
                    if vend.get('codVendedor') == cod_vendedor:
                        vendedor_encontrado = vend
                        break
                
                if not vendedor_encontrado:
                    print("Vendedor não encontrado.")
                    continue
                
                print(f"\nDados atuais do vendedor {vendedor_encontrado.get('nome', 'N/A')}:")
                print(f"Código: {vendedor_encontrado.get('codVendedor', 'N/A')}")
                print(f"Email: {vendedor_encontrado.get('email', 'N/A')}")
                
                print("\nDigite os novos dados (deixe vazio para manter o atual):")
                novo_nome = input(f"Novo nome (atual: {vendedor_encontrado.get('nome', 'N/A')}): ")
                novo_email = input(f"Novo email (atual: {vendedor_encontrado.get('email', 'N/A')}): ")
                
                novos_dados = {}
                if novo_nome:
                    novos_dados['nome'] = novo_nome
                if novo_email:
                    novos_dados['email'] = novo_email
                
                if novos_dados:
                    result = vendedor.update_vendedor(cod_vendedor, novos_dados)
                    if result.modified_count > 0:
                        print("Vendedor atualizado com sucesso!")
                    else:
                        print("Nenhuma alteração foi feita.")
                else:
                    print("Nenhuma alteração foi fornecida.")
            
            elif (sub == '4'):
                print("=== DELETE VENDEDOR ===")
                cod_vendedor = input("Digite o código do vendedor a ser deletado: ")
                
                vendedores = vendedor.find_vendedor()
                vendedor_encontrado = None
                for vend in vendedores:
                    if vend.get('codVendedor') == cod_vendedor:
                        vendedor_encontrado = vend
                        break
                
                if not vendedor_encontrado:
                    print("Vendedor não encontrado.")
                    continue
                
                confirmacao = input(f"Tem certeza que deseja deletar o vendedor {vendedor_encontrado.get('nome', 'N/A')} (Código: {cod_vendedor})? (s/N): ")
                if confirmacao.lower() in ['s', 'sim', 'y', 'yes']:
                    result = vendedor.delete_vendedor(cod_vendedor)
                    if result.deleted_count > 0:
                        print("Vendedor deletado com sucesso!")
                    else:
                        print("Vendedor não encontrado ou não foi deletado.")
                else:
                    print("Operação cancelada.")
            
            elif (sub.lower() == 'v'):
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida!")
    
    def product_crud_menu(self):
        """Product CRUD operations"""
        while True:
            print("\n" + "="*30)
            print("      MENU PRODUTO")
            print("="*30)
            print("1 - Create Produto")
            print("2 - Read Produto")
            print("3 - Update Produto")
            print("4 - Delete Produto")
            print("V - Voltar")
            print("="*30)
            sub = input("Digite a opção desejada: ")
            
            if (sub == '1'):
                print("=== CREATE PRODUTO ===")
                cod_produto = input("Digite o código do produto: ")
                descricao = input("Digite a descrição: ")
                
                while True:
                    try:
                        preco = float(input("Digite o preço: "))
                        if preco < 0:
                            print("O preço deve ser um número positivo.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, digite um número válido para o preço.")
                
                while True:
                    try:
                        estoque = int(input("Digite a quantidade em estoque: "))
                        if estoque < 0:
                            print("O estoque deve ser um número inteiro positivo.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, digite um número inteiro válido para o estoque.")
                
                produto_data = produto.create_produto_schema(cod_produto, descricao, preco, estoque)
                success, result = produto.insert_produto(produto_data)
                
                if success:
                    print(f"Produto criado com sucesso! ID: {result}")
                else:
                    print(f"Erro ao criar produto: {result}")
            
            elif (sub == '2'):
                print("=== READ PRODUTO ===")
                descricao = input("Digite a descrição do produto (ou deixe vazio para listar todos): ")
                produtos = produto.find_produto(descricao if descricao else None)
                
                if produtos:
                    print(f"\nEncontrados {len(produtos)} produto(s):")
                    for prod in produtos:
                        print(f"- Descrição: {prod.get('descricao', 'N/A')}")
                        print(f"  Código: {prod.get('codProduto', 'N/A')}")
                        print(f"  Preço: R$ {prod.get('preco', 0):.2f}")
                        print(f"  Estoque: {prod.get('estoque', 0)}")
                        print(f"  ID: {prod.get('_id', 'N/A')}")
                        print()
                else:
                    print("Nenhum produto encontrado.")
            
            elif (sub == '3'):
                print("=== UPDATE PRODUTO ===")
                cod_produto = input("Digite o código do produto a ser atualizado: ")
                
                produtos = produto.find_produto()
                produto_encontrado = None
                for prod in produtos:
                    if prod.get('codProduto') == cod_produto:
                        produto_encontrado = prod
                        break
                
                if not produto_encontrado:
                    print("Produto não encontrado.")
                    continue
                
                print(f"\nDados atuais do produto {produto_encontrado.get('descricao', 'N/A')}:")
                print(f"Código: {produto_encontrado.get('codProduto', 'N/A')}")
                print(f"Preço: R$ {produto_encontrado.get('preco', 0):.2f}")
                print(f"Estoque: {produto_encontrado.get('estoque', 0)}")
                
                print("\nDigite os novos dados (deixe vazio para manter o atual):")
                nova_descricao = input(f"Nova descrição (atual: {produto_encontrado.get('descricao', 'N/A')}): ")
                
                novo_preco = None
                preco_input = input(f"Novo preço (atual: R$ {produto_encontrado.get('preco', 0):.2f}): ")
                if preco_input:
                    while True:
                        try:
                            novo_preco = float(preco_input)
                            if novo_preco < 0:
                                print("O preço deve ser um número positivo.")
                                preco_input = input("Digite o novo preço: ")
                                continue
                            break
                        except ValueError:
                            print("Por favor, digite um número válido para o preço.")
                            preco_input = input("Digite o novo preço: ")
                
                novo_estoque = None
                estoque_input = input(f"Novo estoque (atual: {produto_encontrado.get('estoque', 0)}): ")
                if estoque_input:
                    while True:
                        try:
                            novo_estoque = int(estoque_input)
                            if novo_estoque < 0:
                                print("O estoque deve ser um número inteiro positivo.")
                                estoque_input = input("Digite o novo estoque: ")
                                continue
                            break
                        except ValueError:
                            print("Por favor, digite um número inteiro válido para o estoque.")
                            estoque_input = input("Digite o novo estoque: ")
                
                novos_dados = {}
                if nova_descricao:
                    novos_dados['descricao'] = nova_descricao
                if novo_preco is not None:
                    novos_dados['preco'] = novo_preco
                if novo_estoque is not None:
                    novos_dados['estoque'] = novo_estoque
                
                if novos_dados:
                    result = produto.update_produto(cod_produto, novos_dados)
                    if result.modified_count > 0:
                        print("Produto atualizado com sucesso!")
                    else:
                        print("Nenhuma alteração foi feita.")
                else:
                    print("Nenhuma alteração foi fornecida.")
            
            elif (sub == '4'):
                print("=== DELETE PRODUTO ===")
                cod_produto = input("Digite o código do produto a ser deletado: ")
                
                produtos = produto.find_produto()
                produto_encontrado = None
                for prod in produtos:
                    if prod.get('codProduto') == cod_produto:
                        produto_encontrado = prod
                        break
                
                if not produto_encontrado:
                    print("Produto não encontrado.")
                    continue
                
                confirmacao = input(f"Tem certeza que deseja deletar o produto '{produto_encontrado.get('descricao', 'N/A')}' (Código: {cod_produto})? (s/N): ")
                if confirmacao.lower() in ['s', 'sim', 'y', 'yes']:
                    result = produto.delete_produto(cod_produto)
                    if result.deleted_count > 0:
                        print("Produto deletado com sucesso!")
                    else:
                        print("Produto não encontrado ou não foi deletado.")
                else:
                    print("Operação cancelada.")
            
            elif (sub.lower() == 'v'):
                print("Voltando ao menu principal...")
                break
            else:
                print("Opção inválida!")
    

def main():
    """Main application entry point"""
    try:
        # Test database connections
        client.admin.command('ping')
        print("✅ MongoDB conectado com sucesso!")
        
        redis_success, redis_message = redis_manager.test_connection()
        if redis_success:
            print(f"✅ {redis_message}")
        else:
            print(f"❌ {redis_message}")
            print("Continuando sem Redis...")
        
        # Start enhanced menu
        menu = EnhancedMenu()
        menu.main_menu()
        
    except Exception as e:
        print(f"❌ Erro ao conectar com o banco de dados: {e}")
        print("Verifique sua conexão com a internet e tente novamente.")

if __name__ == "__main__":
    main()
