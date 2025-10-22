# Sistema Mercado Livre - Redis + MongoDB

Sistema de e-commerce com autenticação Redis e carrinho persistente.

## 🚀 Como Rodar

### 1. Instalar Dependências
```bash
pip install pymongo redis certifi
```

### 2. Executar o Sistema
```bash
python3 main.py
```

### 3. Fazer Login
- **Nome**: admin
- **CPF**: 000.000.000-00 (opcional)

## 📋 Funcionalidades

### Menu Principal
1. **CRUD Usuário** - Criar, listar, atualizar, deletar usuários
2. **CRUD Vendedor** - Gerenciar vendedores
3. **CRUD Produto** - Gerenciar produtos
4. **🛒 Carrinho** - Adicionar/remover produtos do carrinho
5. **💳 Finalizar Compra** - Completar compra e salvar no histórico
6. **Logout** - Sair do sistema

### Recursos Especiais
- ✅ **Login com Redis**: Sessões persistentes
- ✅ **Carrinho Redis**: Carrinho salvo entre sessões
- ✅ **Histórico de Compras**: Compras salvas no perfil do usuário
- ✅ **Admin Automático**: Usuário admin criado automaticamente

## 🛒 Como Usar o Carrinho

1. **Adicionar Produto**: Menu 4 → opção 2 → escolher produto
2. **Ver Carrinho**: Menu 4 → opção 1
3. **Finalizar Compra**: Menu 5 → confirmar com "s" → escolher vendedor
4. **Ver Histórico**: Menu 1 → opção 2 → listar usuários

## 🔧 Configuração

### MongoDB
- Conecta automaticamente com Atlas
- Banco: `mercadolivre`

### Redis
- Host: redis-17140.c283.us-east-1-4.ec2.redns.redis-cloud.com
- Porta: 17140
- Usuário: default
- Senha: configurada automaticamente

## 📁 Estrutura do Projeto

```
Ex3 - Redis/
├── main.py                 # ← EXECUTAR ESTE ARQUIVO
├── src/
│   ├── enhanced_menu.py   # Menu principal
│   ├── config.py          # Configurações MongoDB + Redis
│   ├── myredis.py         # Gerenciador Redis
│   ├── mymongo.py         # Gerenciador MongoDB
│   ├── seed_admin_user.py # Script de usuário admin
│   ├── auth/              # Autenticação
│   ├── cart/              # Carrinho
│   └── models/             # Modelos de dados
└── README.md              # Este arquivo
```

## 🎯 Exemplo de Uso

1. Execute: `python3 main.py`
2. Login: admin / 000.000.000-00
3. Criar produto: Menu 3 → opção 1
4. Adicionar ao carrinho: Menu 4 → opção 2
5. Finalizar compra: Menu 5 → "s" → código vendedor
6. Ver histórico: Menu 1 → opção 2

## ⚠️ Importante

- O usuário admin é criado automaticamente
- O carrinho persiste entre sessões
- As compras ficam salvas no histórico do usuário
- Sistema funciona offline (Redis + MongoDB na nuvem)

## 🐛 Problemas?

- Verifique se as dependências estão instaladas
- Confirme a conexão com internet
- Use Python 3.6 ou superior