# Sistema Mercado Livre - Redis Integration

Este projeto agora inclui integração com Redis para autenticação de usuários, gerenciamento de sessões e persistência de carrinho de compras.

## 🚀 Funcionalidades Implementadas

### 1. **Autenticação e Sessões**
- Login de usuários com persistência de sessão no Redis
- Logout automático após timeout (1 hora)
- Verificação de usuário logado
- Gerenciamento de sessões ativas

### 2. **Carrinho de Compras Persistente**
- Adicionar produtos ao carrinho
- Remover produtos do carrinho
- Atualizar quantidades
- Persistência automática no Redis (24 horas)
- Cálculo automático de totais

### 3. **Integração com Sistema Existente**
- Mantém compatibilidade com MongoDB
- Integra com sistema de usuários existente
- Funciona com produtos e vendedores cadastrados

## 📁 Arquivos Criados/Modificados

### Novos Arquivos:
- `auth.py` - Gerenciamento de autenticação
- `cart_manager.py` - Gerenciamento de carrinho
- `enhanced_menu.py` - Menu principal com Redis
- `test_redis.py` - Testes de funcionalidade
- `requirements.txt` - Dependências do projeto

### Arquivos Modificados:
- `config.py` - Adicionada configuração Redis
- `myredis.py` - Implementação completa do RedisManager

## 🔧 Configuração

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configuração Redis
O Redis já está configurado com suas credenciais:
- **Host**: redis-17140.c283.us-east-1-4.ec2.redns.redis-cloud.com
- **Port**: 17140
- **Username**: default
- **Password**: zH4Q0dGD59UWxxP7zv5hODcZz05wo0ML

### 3. Testar Conexão
```bash
python test_redis.py
```

## 🎯 Como Usar

### Menu Original (menu.py)
- Mantém todas as funcionalidades CRUD originais
- Sem autenticação Redis

### Menu Aprimorado (enhanced_menu.py)
- **Login obrigatório** para acessar funcionalidades
- **Carrinho persistente** entre sessões
- **Checkout integrado** com sistema de compras

```bash
python enhanced_menu.py
```

## 🔄 Fluxo de Uso

1. **Login**: Usuário faz login com nome (e CPF se necessário)
2. **Sessão**: Sistema mantém sessão ativa no Redis
3. **Carrinho**: Usuário pode adicionar/remover produtos
4. **Persistência**: Carrinho salvo automaticamente
5. **Checkout**: Finalizar compra e limpar carrinho
6. **Logout**: Sessão encerrada e dados limpos

## 🛒 Funcionalidades do Carrinho

### Adicionar Produto
- Seleciona produto da lista disponível
- Define quantidade
- Verifica estoque automaticamente
- Atualiza total automaticamente

### Gerenciar Carrinho
- Ver itens adicionados
- Remover produtos específicos
- Atualizar quantidades
- Limpar carrinho completo

### Persistência
- Carrinho salvo automaticamente
- Mantido por 24 horas
- Recuperado no próximo login

## 🔐 Segurança

### Sessões
- Timeout automático (1 hora de inatividade)
- Limpeza automática de sessões expiradas
- Verificação de sessão ativa

### Dados
- Sessões criptografadas no Redis
- Dados de carrinho isolados por usuário
- Limpeza automática após logout

## 📊 Estrutura Redis

### Chaves Utilizadas:
- `session:{user_id}` - Dados da sessão
- `cart:{user_id}` - Carrinho do usuário
- `active_sessions` - Lista de sessões ativas

### Timeouts:
- **Sessão**: 3600 segundos (1 hora)
- **Carrinho**: 86400 segundos (24 horas)

## 🧪 Testes

Execute os testes para verificar a funcionalidade:

```bash
python test_redis.py
```

Os testes verificam:
- ✅ Conexão com Redis
- ✅ Criação/recuperação de sessões
- ✅ Operações de carrinho
- ✅ Limpeza de dados

## 🚨 Solução de Problemas

### Erro de Conexão Redis
- Verifique se as credenciais estão corretas
- Teste a conectividade de rede
- Execute `python test_redis.py`

### Sessão Perdida
- Sessões expiram após 1 hora de inatividade
- Faça login novamente
- Carrinho será recuperado automaticamente

### Carrinho Não Salva
- Verifique se o usuário está logado
- Teste a conexão Redis
- Verifique logs de erro

## 📈 Próximos Passos

1. **Implementar notificações** de produtos em promoção
2. **Adicionar favoritos** persistentes
3. **Histórico de navegação** do usuário
4. **Analytics** de comportamento de compra
5. **Cache** de produtos mais acessados

## 💡 Vantagens da Implementação

- **Performance**: Redis é muito mais rápido que MongoDB para sessões
- **Escalabilidade**: Suporta múltiplos usuários simultâneos
- **Persistência**: Carrinho mantido entre sessões
- **Segurança**: Sessões com timeout automático
- **Flexibilidade**: Fácil expansão para novas funcionalidades

---

**Desenvolvido para o Exercício 3 - Redis (NoSQL)**
**Fatec - DSM - 3º Semestre**
