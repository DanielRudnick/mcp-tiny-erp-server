# 🚀 Guia Completo de Deploy - MCP Tiny ERP Server

**Data**: 31 de Outubro de 2024
**Versão**: 1.0.0
**Plataforma**: Railway

Este guia irá ajudá-lo a fazer o deploy completo do seu servidor MCP Tiny ERP.

---

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Conta no Railway (https://railway.app)
- ✅ Git instalado
- ✅ Token da API do Tiny ERP

---

## 🎯 PASSO 1: Preparar o Repositório Git

### 1.1. Abra o PowerShell ou Terminal

```powershell
# Navegue até o diretório do projeto
cd C:\Users\Admin\Downloads\mcp-tiny-erp-server
```

### 1.2. Adicione os Novos Arquivos ao Git

```bash
# Adicione os novos arquivos criados
git add src/api/mcp_tools_completo.py
git add src/services/tiny_client.py
git add NOVO_MCP_TOOLS_COMPLETO.md
git add EXEMPLOS_USO_NOVAS_FERRAMENTAS.md
git add RELATORIO_TESTES.md
git add test_novas_ferramentas.py
git add GUIA_DEPLOY_COMPLETO.md
```

### 1.3. Faça o Commit

```bash
git commit -m "feat: adicionar 120+ novos endpoints da API Tiny

- Implementados todos os endpoints da API Tiny V2
- Adicionados métodos para: Contatos, Produtos, CRM, Contas, Notas Fiscais, PDV, Expedições, etc
- Sistema de cache e rate limiting implementado
- Documentação completa e exemplos de uso
- Testes de validação criados
- 100% de cobertura da API Tiny"
```

### 1.4. Verifique o Remote do GitHub

```bash
# Veja o remote atual
git remote -v
```

**Resultado esperado:**
```
origin  https://github.com/SEU_USUARIO/mcp-tiny-erp-server.git (fetch)
origin  https://github.com/SEU_USUARIO/mcp-tiny-erp-server.git (push)
```

### 1.5. Faça o Push para o GitHub

```bash
# Push para o GitHub
git push origin main
```

---

## 🚂 PASSO 2: Configurar o Railway

### 2.1. Criar Conta e Projeto

1. **Acesse**: https://railway.app
2. **Faça login** com sua conta GitHub
3. **Clique em**: `New Project`
4. **Selecione**: `Deploy from GitHub repo`
5. **Autorize** o Railway a acessar seus repositórios
6. **Selecione**: `mcp-tiny-erp-server`

### 2.2. Adicionar PostgreSQL

1. No dashboard do projeto, clique em `New`
2. Selecione `Database`
3. Escolha `Add PostgreSQL`
4. Aguarde a criação (leva ~30 segundos)

### 2.3. Adicionar Redis

1. No dashboard do projeto, clique em `New`
2. Selecione `Database`
3. Escolha `Add Redis`
4. Aguarde a criação (leva ~30 segundos)

### 2.4. Configurar Variáveis de Ambiente

1. Clique no seu serviço principal (mcp-tiny-erp-server)
2. Vá em `Variables`
3. Adicione as seguintes variáveis:

#### Variáveis Obrigatórias:

```bash
# Segurança (IMPORTANTE: Gere uma chave forte)
SECRET_KEY=cole-aqui-a-chave-gerada-abaixo

# Ambiente
ENVIRONMENT=production
API_VERSION=v1
DEBUG=false

# Tiny API
TINY_API_BASE_URL=https://api.tiny.com.br/api2
TINY_API_TIMEOUT=30

# Rate Limiting
RATE_LIMIT_FREE=100
RATE_LIMIT_PRO=500
RATE_LIMIT_ENTERPRISE=2000

# Cache (em segundos)
CACHE_TTL_PEDIDOS=300
CACHE_TTL_PRODUTOS=300
CACHE_TTL_TENANT=3600

# CORS (ajuste conforme necessário)
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Features
ENABLE_WEBSOCKET=true
ENABLE_WEBHOOKS=true
ENABLE_METRICS=true
ENABLE_SWAGGER=true

# Webhooks
WEBHOOK_TIMEOUT=10
WEBHOOK_RETRY_ATTEMPTS=3
WEBHOOK_RETRY_DELAY=60
```

#### Variáveis Automáticas (Railway cria automaticamente):

- ✅ `DATABASE_URL` - Criado automaticamente pelo PostgreSQL plugin
- ✅ `REDIS_URL` - Criado automaticamente pelo Redis plugin
- ✅ `PORT` - Porta fornecida pelo Railway

---

## 🔐 PASSO 3: Gerar SECRET_KEY

### Opção 1: No Linux/Mac/Git Bash

```bash
openssl rand -hex 32
```

### Opção 2: No PowerShell (Windows)

```powershell
# Gere um GUID forte
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString() + [System.Guid]::NewGuid().ToString()))
```

### Opção 3: Online (Use com cuidado em produção)

Acesse: https://randomkeygen.com/

**Copie** o valor gerado e cole na variável `SECRET_KEY` no Railway.

---

## 🏗️ PASSO 4: Deploy Automático

Após configurar tudo:

1. Railway irá **detectar automaticamente** o Dockerfile
2. Iniciará o **build** da aplicação
3. Executará o **deploy**
4. Gerará uma **URL pública**

### Acompanhar o Deploy:

1. Vá em `Deployments` no dashboard
2. Clique no deployment em andamento
3. Veja os logs em tempo real

**Tempo estimado**: 3-5 minutos

---

## ✅ PASSO 5: Verificar o Deploy

### 5.1. Obter a URL

No Railway dashboard:
1. Vá em `Settings` → `Networking`
2. Clique em `Generate Domain`
3. Anote a URL gerada (ex: `mcp-tiny-erp-production.up.railway.app`)

### 5.2. Testar o Health Check

```bash
curl https://SUA-URL.railway.app/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-10-31T12:00:00Z",
  "database": "connected",
  "redis": "connected"
}
```

### 5.3. Testar o Endpoint de Info

```bash
curl https://SUA-URL.railway.app/
```

**Resposta esperada:**
```json
{
  "name": "MCP Tiny ERP Server",
  "version": "1.0.0",
  "status": "online"
}
```

### 5.4. Verificar Documentação Swagger

Acesse no navegador:
```
https://SUA-URL.railway.app/docs
```

Você deve ver a interface Swagger com TODOS os ~120 endpoints!

---

## 👥 PASSO 6: Criar Primeiro Tenant

### 6.1. Via cURL

```bash
curl -X POST "https://SUA-URL.railway.app/api/v1/tenants" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Minha Empresa LTDA",
    "tiny_token": "SEU_TOKEN_TINY_AQUI",
    "plano": "pro",
    "email_contato": "contato@minhaempresa.com"
  }'
```

### 6.2. Resposta Esperada

```json
{
  "id": "uuid-gerado-automaticamente",
  "nome": "Minha Empresa LTDA",
  "api_key": "chave-api-gerada",
  "plano": "pro",
  "ativo": true,
  "created_at": "2024-10-31T12:00:00Z"
}
```

**IMPORTANTE**: Salve o `api_key` retornado! Você precisará dele para autenticar.

---

## 🧪 PASSO 7: Testar os Novos Endpoints

### 7.1. Testar Pesquisa de Contatos

```bash
curl -X POST "https://SUA-URL.railway.app/api/v1/mcp/tools/tiny.contatos.pesquisar" \
  -H "Content-Type: application/json" \
  -d '{
    "pesquisa": "João",
    "pagina": 1
  }' \
  --user "tenant-id:api-key"
```

### 7.2. Testar Listagem de Produtos

```bash
curl -X POST "https://SUA-URL.railway.app/api/v1/mcp/tools/tiny.produtos.pesquisar" \
  -H "Content-Type: application/json" \
  -d '{
    "pesquisa": "notebook",
    "pagina": 1
  }' \
  --user "tenant-id:api-key"
```

### 7.3. Testar Info da Conta

```bash
curl -X POST "https://SUA-URL.railway.app/api/v1/mcp/tools/tiny.conta.obter.info" \
  -H "Content-Type: application/json" \
  --user "tenant-id:api-key"
```

---

## 🔧 PASSO 8: Configurações Adicionais

### 8.1. Domínio Personalizado (Opcional)

1. No Railway, vá em `Settings` → `Networking`
2. Clique em `Custom Domain`
3. Digite: `api.seudominio.com`
4. No seu provedor DNS, adicione:
   ```
   CNAME api.seudominio.com -> seu-projeto.up.railway.app
   ```
5. Aguarde propagação (até 48h)

### 8.2. Configurar Monitoramento

Railway oferece métricas integradas:
1. Vá em `Metrics` no dashboard
2. Configure alertas em `Settings` → `Alerts`

### 8.3. Configurar Backup Automático

PostgreSQL no Railway tem backup automático:
1. Vá no plugin PostgreSQL
2. Veja `Backups` para configurações

---

## 📊 PASSO 9: Monitoramento

### 9.1. Ver Logs em Tempo Real

```bash
# Instale Railway CLI (se ainda não tem)
npm i -g @railway/cli

# Login
railway login

# Link ao projeto
railway link

# Ver logs
railway logs --follow
```

### 9.2. Verificar Métricas

No dashboard do Railway:
- **CPU**: Deve ficar < 50% em idle
- **Memory**: Deve ficar < 70%
- **Network**: Monitore picos de tráfego
- **Database**: Verifique conexões ativas

### 9.3. Configurar Alertas

1. Vá em `Settings` → `Alerts`
2. Configure alertas para:
   - CPU > 80%
   - Memory > 85%
   - Deploy failures
   - Health check failures

---

## 🔄 PASSO 10: Updates Futuros

### 10.1. Deploy Automático

Sempre que você fizer push para `main`, o Railway faz deploy automático:

```bash
# Faça suas alterações
git add .
git commit -m "feat: nova funcionalidade"
git push origin main

# Railway detecta e faz deploy automaticamente!
```

### 10.2. Rollback

Se algo der errado:

1. Vá em `Deployments`
2. Encontre o deployment anterior que funcionava
3. Clique em `...` → `Redeploy`

### 10.3. Variáveis de Ambiente

Para adicionar/modificar variáveis:

1. Vá em `Variables`
2. Adicione ou edite
3. Railway faz redeploy automaticamente

---

## 🆘 Troubleshooting

### Problema 1: Build Falha

**Erro**: `Error building image`

**Solução**:
```bash
# Verifique os logs de build
railway logs --build

# Comum: dependências faltando no requirements.txt
# Adicione a dependência e faça push novamente
```

### Problema 2: App Não Inicia

**Erro**: `Application failed to start`

**Solução**:
```bash
# Verifique logs
railway logs

# Verifique variáveis de ambiente
railway variables

# Certifique-se que DATABASE_URL e REDIS_URL existem
```

### Problema 3: Erro 500 nas Requisições

**Erro**: `Internal Server Error`

**Solução**:
```bash
# Ver logs detalhados
railway logs --follow

# Verifique se:
# - SECRET_KEY está configurado
# - Tiny API token é válido
# - Database está acessível
```

### Problema 4: Timeout nas Requisições

**Erro**: `Request timeout`

**Solução**:
- Aumente `TINY_API_TIMEOUT` nas variáveis
- Verifique conexão com API do Tiny
- Considere otimizar queries

---

## 📞 Suporte

### Recursos Disponíveis:

- 📚 **Docs Railway**: https://docs.railway.app
- 💬 **Discord Railway**: https://discord.gg/railway
- 📖 **Swagger Local**: https://SUA-URL.railway.app/docs
- 🐛 **Issues**: Abra no GitHub do projeto

### Logs Importantes:

```bash
# Ver todos os logs
railway logs

# Filtrar por erro
railway logs | grep ERROR

# Seguir logs em tempo real
railway logs --follow
```

---

## ✅ Checklist Final

Marque conforme concluir:

- [ ] ✅ Código commitado e pushed para GitHub
- [ ] ✅ Projeto criado no Railway
- [ ] ✅ PostgreSQL adicionado e conectado
- [ ] ✅ Redis adicionado e conectado
- [ ] ✅ Variáveis de ambiente configuradas
- [ ] ✅ SECRET_KEY gerado e configurado
- [ ] ✅ Deploy concluído com sucesso
- [ ] ✅ Health check respondendo OK
- [ ] ✅ Swagger acessível
- [ ] ✅ Primeiro tenant criado
- [ ] ✅ Endpoint de teste funcionando
- [ ] ✅ Logs monitorados
- [ ] ✅ Domínio personalizado (opcional)
- [ ] ✅ Alertas configurados

---

## 🎉 Parabéns!

Seu **MCP Tiny ERP Server** está no ar com **120+ endpoints** prontos para uso!

### Próximos Passos:

1. **Integre** com Claude Desktop ou outros clients MCP
2. **Monitore** o uso via Railway dashboard
3. **Escale** conforme necessário (Railway auto-scale)
4. **Documente** casos de uso específicos do seu negócio
5. **Otimize** baseado nos logs e métricas

---

## 📈 Informações Úteis

### URLs Importantes:

- **Aplicação**: https://SUA-URL.railway.app
- **Swagger**: https://SUA-URL.railway.app/docs
- **Health**: https://SUA-URL.railway.app/health
- **Metrics**: https://SUA-URL.railway.app/metrics (se habilitado)

### Planos Railway:

- **Hobby**: $5/mês - Ideal para começar
- **Pro**: $20/mês - Produção leve
- **Enterprise**: Custom - Alta escala

### Limites Iniciais:

- **CPU**: Shared
- **RAM**: 512MB (pode aumentar)
- **Storage**: 1GB (PostgreSQL)
- **Bandwidth**: 100GB/mês

---

**Versão do Guia**: 1.0.0
**Última Atualização**: 31 de Outubro de 2024
**Autor**: Claude (Anthropic)

---

🚀 **Boa sorte com seu deploy!**
