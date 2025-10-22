from models import usuario, vendedor, produto, compra
from config import client
from config import db


def abrir_menu():
    key = ""
    sub = ""
    while (key.upper() != 'S'):
        print("\n" + "="*50)
        print("           SISTEMA MERCADO LIVRE")
        print("="*50)
        print("1 - CRUD Usuário")
        print("2 - CRUD Vendedor")
        print("3 - CRUD Produto")
        print("4 - CRUD Compra")
        print("S - Sair")
        print("="*50)
        key = input("Digite a opção desejada: ")

        if (key == '1'):
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
                            # Se enderecos é uma lista de strings
                            if isinstance(enderecos[0], str):
                                print(f"  Endereços: {', '.join(enderecos)}")
                            # Se enderecos é uma lista de dicionários
                            else:
                                enderecos_str = [str(end) for end in enderecos]
                                print(f"  Endereços: {', '.join(enderecos_str)}")
                        else:
                            print(f"  Endereços: Nenhum")
                        print(f"  ID: {user.get('_id', 'N/A')}")
                        print()
                else:
                    print("Nenhum usuário encontrado.")
            
            elif (sub == '3'):
                print("=== UPDATE USUÁRIO ===")
                nome = input("Digite o nome do usuário a ser atualizado: ")
                
                # Primeiro, buscar o usuário para mostrar os dados atuais
                usuarios = usuario.find_usuario(nome)
                if not usuarios:
                    print("Usuário não encontrado.")
                    continue
                
                user = usuarios[0]  # Pegar o primeiro resultado
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
                
                # Coletar novos dados
                print("\nDigite os novos dados (deixe vazio para manter o atual):")
                novo_sobrenome = input(f"Novo sobrenome (atual: {user.get('sobrenome', 'N/A')}): ")
                novo_cpf = input(f"Novo CPF (atual: {user.get('cpf', 'N/A')}): ")
                
                # Mostrar endereços atuais de forma segura
                enderecos_atuais = user.get('end', [])
                if enderecos_atuais:
                    if isinstance(enderecos_atuais[0], str):
                        enderecos_str = ', '.join(enderecos_atuais)
                    else:
                        enderecos_str = ', '.join([str(end) for end in enderecos_atuais])
                else:
                    enderecos_str = "Nenhum"
                
                novos_enderecos = input(f"Novos endereços (atual: {enderecos_str}): ")
                
                # Preparar dados para atualização
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
                
                # Confirmar antes de deletar
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
                continue
            else:
                print("Opção inválida!")
                
        elif (key == '2'):
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
                
                # Primeiro, buscar o vendedor para mostrar os dados atuais
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
                
                # Coletar novos dados
                print("\nDigite os novos dados (deixe vazio para manter o atual):")
                novo_nome = input(f"Novo nome (atual: {vendedor_encontrado.get('nome', 'N/A')}): ")
                novo_email = input(f"Novo email (atual: {vendedor_encontrado.get('email', 'N/A')}): ")
                
                # Preparar dados para atualização
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
                
                # Buscar o vendedor para mostrar os dados antes de deletar
                vendedores = vendedor.find_vendedor()
                vendedor_encontrado = None
                for vend in vendedores:
                    if vend.get('codVendedor') == cod_vendedor:
                        vendedor_encontrado = vend
                        break
                
                if not vendedor_encontrado:
                    print("Vendedor não encontrado.")
                    continue
                
                # Confirmar antes de deletar
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
                continue
            else:
                print("Opção inválida!")   
        elif (key == '3'):
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
                
                # Validar preço
                while True:
                    try:
                        preco = float(input("Digite o preço: "))
                        if preco < 0:
                            print("O preço deve ser um número positivo.")
                            continue
                        break
                    except ValueError:
                        print("Por favor, digite um número válido para o preço.")
                
                # Validar estoque
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
                
                # Primeiro, buscar o produto para mostrar os dados atuais
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
                
                # Coletar novos dados
                print("\nDigite os novos dados (deixe vazio para manter o atual):")
                nova_descricao = input(f"Nova descrição (atual: {produto_encontrado.get('descricao', 'N/A')}): ")
                
                # Atualizar preço
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
                
                # Atualizar estoque
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
                
                # Preparar dados para atualização
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
                
                # Buscar o produto para mostrar os dados antes de deletar
                produtos = produto.find_produto()
                produto_encontrado = None
                for prod in produtos:
                    if prod.get('codProduto') == cod_produto:
                        produto_encontrado = prod
                        break
                
                if not produto_encontrado:
                    print("Produto não encontrado.")
                    continue
                
                # Confirmar antes de deletar
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
                continue
            else:
                print("Opção inválida!")
                
        elif (key == '4'):
            print("\n" + "="*30)
            print("      MENU COMPRA")
            print("="*30)
            print("1 - Create Compra")
            print("2 - Read Compra")
            print("3 - Update Compra")
            print("4 - Delete Compra")
            print("V - Voltar")
            print("="*30)
            sub = input("Digite a opção desejada: ")
            
            if (sub == '1'):
                print("=== CREATE COMPRA ===")
                
                # Buscar usuário
                nome_usuario = input("Digite o nome do usuário: ")
                usuarios = usuario.find_usuario(nome_usuario)
                if not usuarios:
                    print("Usuário não encontrado.")
                    continue
                usuario_compra = usuarios[0]
                
                # Buscar vendedor
                cod_vendedor = input("Digite o código do vendedor: ")
                vendedores = vendedor.find_vendedor()
                vendedor_compra = None
                for vend in vendedores:
                    if vend.get('codVendedor') == cod_vendedor:
                        vendedor_compra = vend
                        break
                
                if not vendedor_compra:
                    print("Vendedor não encontrado.")
                    continue
                
                # Criar compra
                compra_data = compra.create_compra_schema()
                compra_data["usuario"] = {
                    "usuarioId": str(usuario_compra.get('_id', '')),
                    "nome": usuario_compra.get('nome', ''),
                    "email": usuario_compra.get('email', '') if usuario_compra.get('email') else 'N/A'
                }
                compra_data["vendedor"] = {
                    "codVendedor": vendedor_compra.get('codVendedor', '')
                }
                compra_data["itens"] = []
                
                # Adicionar produtos à compra
                print("\nAdicionando produtos à compra (digite 'finalizar' para terminar):")
                
                # Buscar todos os produtos disponíveis uma vez
                produtos_disponiveis = produto.find_produto()
                
                while True:
                    # Mostrar produtos disponíveis
                    print("\n" + "="*60)
                    print("PRODUTOS DISPONÍVEIS:")
                    print("="*60)
                    if produtos_disponiveis:
                        for prod in produtos_disponiveis:
                            estoque = prod.get('estoque', 0)
                            status_estoque = "✅ Disponível" if estoque > 0 else "❌ Sem estoque"
                            print(f"Código: {prod.get('codProduto', 'N/A')}")
                            print(f"  Descrição: {prod.get('descricao', 'N/A')}")
                            print(f"  Preço: R$ {prod.get('preco', 0):.2f}")
                            print(f"  Estoque: {estoque} - {status_estoque}")
                            print("-" * 40)
                    else:
                        print("Nenhum produto disponível.")
                    print("="*60)
                    
                    # Mostrar resumo do carrinho atual
                    if compra_data["itens"]:
                        print("\nCARRINHO ATUAL:")
                        print("-" * 30)
                        total_carrinho = 0
                        for item in compra_data["itens"]:
                            subtotal = item.get('preco', 0) * item.get('quantidade', 0)
                            total_carrinho += subtotal
                            print(f"• {item.get('descricao')} x{item.get('quantidade')} = R$ {subtotal:.2f}")
                        print(f"TOTAL: R$ {total_carrinho:.2f}")
                        print("-" * 30)

                    cod_produto = input("Digite o código do produto (ou 'finalizar'): ")
                    if cod_produto.lower() == 'finalizar':
                        break
                    
                    # Buscar produto na lista já carregada
                    produto_encontrado = None
                    for prod in produtos_disponiveis:
                        if prod.get('codProduto') == cod_produto:
                            produto_encontrado = prod
                            break
                    
                    if not produto_encontrado:
                        print("Produto não encontrado.")
                        continue
                    
                    # Verificar estoque
                    disponivel, msg = produto.verificar_disponibilidade(produto_encontrado, 1)
                    if not disponivel:
                        print(f"Produto não disponível: {msg}")
                        continue
                    
                    # Solicitar quantidade
                    while True:
                        try:
                            quantidade = int(input(f"Digite a quantidade (estoque disponível: {produto_encontrado.get('estoque', 0)}): "))
                            if quantidade <= 0:
                                print("A quantidade deve ser positiva.")
                                continue
                            
                            # Verificar se há estoque suficiente
                            disponivel, msg = produto.verificar_disponibilidade(produto_encontrado, quantidade)
                            if not disponivel:
                                print(f"Estoque insuficiente: {msg}")
                                continue
                            break
                        except ValueError:
                            print("Por favor, digite um número válido.")
                    
                    # Adicionar item à compra
                    sucesso, msg = compra.adicionar_item_compra(compra_data, produto_encontrado, quantidade)
                    print(f"Item adicionado: {produto_encontrado.get('descricao')} x{quantidade}")
                
                # Verificar se há itens na compra
                if not compra_data["itens"]:
                    print("Compra cancelada: nenhum item foi adicionado.")
                    continue
                
                # Finalizar compra
                sucesso, msg = compra.finalizar_compra(compra_data)
                if not sucesso:
                    print(f"Erro ao finalizar compra: {msg}")
                    continue
                
                # Inserir compra no banco
                success, result = compra.insert_compra(compra_data)
                if success:
                    print(f"Compra criada com sucesso! ID: {result}")
                    print(f"Total: R$ {compra_data['precoTotal']:.2f}")
                    
                    # Atualizar histórico do usuário
                    sucesso_hist, msg_hist = compra.add_compra_to_usuario(nome_usuario, compra_data)
                    if sucesso_hist:
                        print("Compra adicionada ao histórico do usuário.")
                    else:
                        print(f"Aviso: {msg_hist}")
                else:
                    print(f"Erro ao criar compra: {result}")
            
            elif (sub == '2'):
                print("=== READ COMPRA ===")
                print("Filtros de busca (deixe vazio para listar todas):")
                nome_usuario = input("Nome do usuário: ")
                data_inicio = input("Data início (DD/MM/YYYY): ")
                data_fim = input("Data fim (DD/MM/YYYY): ")
                
                compras = compra.find_compra(
                    nome_usuario if nome_usuario else None,
                    data_inicio if data_inicio else None,
                    data_fim if data_fim else None
                )
                
                if compras:
                    print(f"\nEncontradas {len(compras)} compra(s):")
                    for comp in compras:
                        print(f"\n--- Compra ID: {comp.get('_id', 'N/A')} ---")
                        print(f"Data: {comp.get('data', 'N/A')}")
                        print(f"Usuário: {comp.get('usuario', {}).get('nome', 'N/A')}")
                        print(f"Vendedor: {comp.get('vendedor', {}).get('codVendedor', 'N/A')}")
                        print(f"Total: R$ {comp.get('precoTotal', 0):.2f}")
                        print("Itens:")
                        for item in comp.get('itens', []):
                            print(f"  - {item.get('descricao', 'N/A')} x{item.get('quantidade', 0)} = R$ {item.get('subtotal', 0):.2f}")
                else:
                    print("Nenhuma compra encontrada.")
            
            elif (sub == '3'):
                print("=== UPDATE COMPRA ===")
                compra_id = input("Digite o ID da compra a ser atualizada: ")
                
                # Buscar compra
                compras = compra.find_compra()
                compra_encontrada = None
                for comp in compras:
                    if str(comp.get('_id')) == compra_id:
                        compra_encontrada = comp
                        break
                
                if not compra_encontrada:
                    print("Compra não encontrada.")
                    continue
                
                print(f"\nDados atuais da compra:")
                print(f"Data: {compra_encontrada.get('data', 'N/A')}")
                print(f"Usuário: {compra_encontrada.get('usuario', {}).get('nome', 'N/A')}")
                print(f"Vendedor: {compra_encontrada.get('vendedor', {}).get('codVendedor', 'N/A')}")
                print(f"Total: R$ {compra_encontrada.get('precoTotal', 0):.2f}")
                
                print("\nOpções de atualização:")
                print("1 - Atualizar vendedor")
                print("2 - Adicionar item")
                print("3 - Remover item")
                opcao_update = input("Digite a opção: ")
                
                novos_dados = {}
                
                if opcao_update == '1':
                    novo_cod_vendedor = input("Digite o novo código do vendedor: ")
                    vendedores = vendedor.find_vendedor()
                    vendedor_encontrado = None
                    for vend in vendedores:
                        if vend.get('codVendedor') == novo_cod_vendedor:
                            vendedor_encontrado = vend
                            break
                    
                    if vendedor_encontrado:
                        novos_dados["vendedor"] = {"codVendedor": novo_cod_vendedor}
                        print("Vendedor atualizado.")
                    else:
                        print("Vendedor não encontrado.")
                        continue
                
                elif opcao_update == '2':
                    cod_produto = input("Digite o código do produto: ")
                    produtos = produto.find_produto()
                    produto_encontrado = None
                    for prod in produtos:
                        if prod.get('codProduto') == cod_produto:
                            produto_encontrado = prod
                            break
                    
                    if produto_encontrado:
                        quantidade = int(input("Digite a quantidade: "))
                        sucesso, msg = compra.adicionar_item_compra(compra_encontrada, produto_encontrado, quantidade)
                        if sucesso:
                            # Recalcular total
                            compra_encontrada["precoTotal"] = compra.calcular_preco_total(compra_encontrada["itens"])
                            novos_dados["itens"] = compra_encontrada["itens"]
                            novos_dados["precoTotal"] = compra_encontrada["precoTotal"]
                            print("Item adicionado.")
                        else:
                            print(f"Erro: {msg}")
                            continue
                    else:
                        print("Produto não encontrado.")
                        continue
                
                elif opcao_update == '3':
                    print("Itens atuais:")
                    for i, item in enumerate(compra_encontrada.get('itens', [])):
                        print(f"{i+1} - {item.get('descricao')} x{item.get('quantidade')}")
                    
                    try:
                        indice = int(input("Digite o número do item a remover: ")) - 1
                        if 0 <= indice < len(compra_encontrada.get('itens', [])):
                            compra_encontrada["itens"].pop(indice)
                            compra_encontrada["precoTotal"] = compra.calcular_preco_total(compra_encontrada["itens"])
                            novos_dados["itens"] = compra_encontrada["itens"]
                            novos_dados["precoTotal"] = compra_encontrada["precoTotal"]
                            print("Item removido.")
                        else:
                            print("Índice inválido.")
                            continue
                    except ValueError:
                        print("Por favor, digite um número válido.")
                        continue
                
                else:
                    print("Opção inválida.")
                    continue
                
                if novos_dados:
                    result = compra.update_compra(compra_encontrada["_id"], novos_dados)
                    if result.modified_count > 0:
                        print("Compra atualizada com sucesso!")
                    else:
                        print("Nenhuma alteração foi feita.")
                else:
                    print("Nenhuma alteração foi fornecida.")
            
            elif (sub == '4'):
                print("=== DELETE COMPRA ===")
                compra_id = input("Digite o ID da compra a ser deletada: ")
                
                # Buscar compra para mostrar dados
                compras = compra.find_compra()
                compra_encontrada = None
                for comp in compras:
                    if str(comp.get('_id')) == compra_id:
                        compra_encontrada = comp
                        break
                
                if not compra_encontrada:
                    print("Compra não encontrada.")
                    continue
                
                print(f"\nDados da compra a ser deletada:")
                print(f"Data: {compra_encontrada.get('data', 'N/A')}")
                print(f"Usuário: {compra_encontrada.get('usuario', {}).get('nome', 'N/A')}")
                print(f"Total: R$ {compra_encontrada.get('precoTotal', 0):.2f}")
                
                # Confirmar antes de deletar
                confirmacao = input(f"Tem certeza que deseja deletar esta compra? (s/N): ")
                if confirmacao.lower() in ['s', 'sim', 'y', 'yes']:
                    result = compra.delete_compra(compra_encontrada["_id"])
                    if result.deleted_count > 0:
                        print("Compra deletada com sucesso!")
                    else:
                        print("Compra não encontrada ou não foi deletada.")
                else:
                    print("Operação cancelada.")
            
            elif (sub.lower() == 'v'):
                print("Voltando ao menu principal...")
                continue
            else:
                print("Opção inválida!")
                
        elif (key.upper() == 'S'):
            print("\nObrigado por usar o Sistema Mercado Livre!")
            print("Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

try:
    client.admin.command('ping')
    print("Banco de dados conectado com sucesso!")
    abrir_menu()
except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")
    print("Verifique sua conexão com a internet e tente novamente.")
    print("Tchau Prof...")