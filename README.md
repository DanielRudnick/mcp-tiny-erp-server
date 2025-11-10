# 🚀 MCP Tiny ERP Server

Servidor MCP (Model Context Protocol) completo para integração com Tiny ERP, implementando **68+ ferramentas** para acesso total à API Tiny.

## ✨ Características

- 🎯 **68+ Ferramentas MCP** cobrindo toda a API Tiny ERP
- 🔐 **Autenticação JWT** com tiny_token integrado
- 📡 **Protocolo MCP 2025-06-18** (streamable HTTP transport)
- 🚀 **Pronto para produção** (Railway, Fly.io, etc)
- 📊 **FastAPI** com documentação automática (Swagger)
- 🔄 **Async/Await** para melhor performance

## 📦 Ferramentas Disponíveis

### Pedidos (7)
- `tiny_pedidos_pesquisar` - Pesquisa pedidos
- `tiny_pedido_obter` - Detalhes do pedido
- `tiny_pedido_incluir` - Criar pedido
- `tiny_pedido_alterar` - Alterar pedido
- `tiny_pedido_alterar_situacao` - Mudar situação
- `tiny_pedido_obter_rastreamento` - Rastreamento

### Produtos (7)
- `tiny_produtos_pesquisar` - Pesquisa produtos
- `tiny_produto_obter` - Detalhes do produto
- `tiny_produto_incluir` - Criar produto
- `tiny_produto_alterar` - Alterar produto
- `tiny_produto_obter_estoque` - Ver estoque
- `tiny_produto_atualizar_estoque` - Atualizar estoque
- `tiny_produto_obter_preco` - Ver preço

### Contatos (4)
- `tiny_contatos_pesquisar` - Pesquisa contatos
- `tiny_contato_obter` - Detalhes do contato
- `tiny_contato_incluir` - Criar contato
- `tiny_contato_alterar` - Alterar contato

### Notas Fiscais (7)
- `tiny_notas_fiscais_pesquisar` - Pesquisa NFe
- `tiny_nota_fiscal_obter` - Detalhes da NFe
- `tiny_nota_fiscal_incluir` - Emitir NFe
- `tiny_nota_fiscal_gerar_pedido` - NFe de pedido
- `tiny_nota_fiscal_enviar_email` - Enviar NFe
- `tiny_nota_fiscal_obter_xml` - Download XML
- `tiny_nota_fiscal_cancelar` - Cancelar NFe

### Financeiro (8)
- `tiny_contas_receber_pesquisar` - Contas a receber
- `tiny_conta_receber_obter` - Detalhes
- `tiny_conta_receber_incluir` - Criar conta
- `tiny_conta_receber_baixar` - Baixar/Quitar
- `tiny_contas_pagar_pesquisar` - Contas a pagar
- `tiny_conta_pagar_obter` - Detalhes
- `tiny_conta_pagar_incluir` - Criar conta
- `tiny_conta_pagar_baixar` - Baixar/Quitar

### CRM (4)
- `tiny_crm_oportunidades_pesquisar` - Oportunidades
- `tiny_crm_oportunidade_obter` - Detalhes
- `tiny_crm_oportunidade_incluir` - Criar
- `tiny_crm_oportunidade_alterar` - Alterar

### E mais de 30 ferramentas para:
- Transportadoras
- Vendedores
- Categorias
- Etiquetas
- Depósitos
- Orçamentos
- Pedidos de Compra
- Manifestos
- Ordens de Serviço
- Kits
- Expedições
- PDV
- Boletos
- Relatórios
- Movimentações de Estoque
- Webhooks
- Integrações
- Marketplace

## 🚀 Deploy Rápido (Railway)

### 1. Preparar Repositório

```bash
# Clone ou navegue até o projeto
cd mcp-tiny-erp-server

# Adicione todos os arquivos
git add -A

# Commit
git commit -m "feat: MCP Tiny ERP Server completo com 68+ ferramentas"

# Push para GitHub
git push origin main
```

### 2. Deploy no Railway

1. Acesse https://railway.app
2. Clique em "New Project"
3. Selecione "Deploy from GitHub"
4. Escolha seu repositório
5. Railway irá detectar o Dockerfile automaticamente
6. Aguarde o deploy (~3-5 minutos)

### 3. Obter URL

Após deploy:
1. Vá em Settings → Networking
2. Clique em "Generate Domain"
3. Sua URL será algo como: `https://seu-projeto.railway.app`

## 🧪 Testar o Servidor

### Health Check

```bash
curl https://SUA-URL.railway.app/health
```

### MCP Info

```bash
curl https://SUA-URL.railway.app/mcp/info
```

### Swagger Docs

Acesse no navegador:
```
https://SUA-URL.railway.app/docs
```

## 🔐 Autenticação

O servidor espera um JWT token com:
- `tenant_id` - ID do tenant
- `tiny_token` - Token da API Tiny

Exemplo de chamada MCP:

```bash
curl -X POST "https://SUA-URL.railway.app/mcp" \
  -H "Authorization: Bearer SEU_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-06-18",
      "capabilities": {},
      "clientInfo": {
        "name": "test-client",
        "version": "1.0.0"
      }
    }
  }'
```

## 🛠️ Desenvolvimento Local

### Requisitos

- Python 3.11+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/mcp-tiny-erp-server.git
cd mcp-tiny-erp-server

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Execute
python -m uvicorn src.main:app --reload
```

Acesse:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 📁 Estrutura do Projeto

```
mcp-tiny-erp-server/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── mcp_server.py      # Servidor MCP
│   │   └── mcp_tools.py       # 68 ferramentas
│   ├── services/
│   │   ├── __init__.py
│   │   └── tiny_client.py     # Cliente API Tiny
│   └── main.py                # Entry point
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
TINY_API_BASE_URL=https://api.tiny.com.br/api2
TINY_API_TIMEOUT=30
ENVIRONMENT=production
DEBUG=false
PORT=8000
CORS_ORIGINS=*
```

## 📝 Licença

MIT License - Veja LICENSE para detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

- 📖 Documentação: `/docs` no servidor
- 🐛 Issues: [GitHub Issues](https://github.com/SEU_USUARIO/mcp-tiny-erp-server/issues)
- 📧 Email: seu-email@exemplo.com

## 🎯 Próximos Passos

- [ ] Adicionar testes unitários
- [ ] Implementar cache Redis
- [ ] Rate limiting por tenant
- [ ] Webhooks do Tiny
- [ ] Logs estruturados
- [ ] Métricas Prometheus

---

**Desenvolvido com ❤️ usando FastAPI e MCP Protocol**
