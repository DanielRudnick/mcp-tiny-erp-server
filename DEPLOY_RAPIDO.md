# ⚡ Deploy Rápido - 5 Minutos

Para quem tem pressa! Siga estes passos:

## 🎯 Opção 1: Script Automático (Recomendado)

### Windows (PowerShell):
```powershell
cd C:\Users\Admin\Downloads\mcp-tiny-erp-server
.\deploy.ps1
```

### Linux/Mac:
```bash
cd ~/Downloads/mcp-tiny-erp-server
chmod +x deploy.sh
./deploy.sh
```

O script vai:
- ✅ Adicionar arquivos ao git
- ✅ Fazer commit
- ✅ Push para GitHub
- ✅ Mostrar próximos passos

---

## 🚀 Opção 2: Manual (3 Comandos)

```bash
# 1. Adicione e commit
git add .
git commit -m "feat: adicionar 120+ endpoints Tiny API"

# 2. Push
git push origin main

# 3. Acesse Railway
# https://railway.app → New Project → Deploy from GitHub
```

---

## ⚙️ Configuração Railway (2 minutos)

### 1. Adicionar Databases:
- PostgreSQL: `New` → `Database` → `PostgreSQL`
- Redis: `New` → `Database` → `Redis`

### 2. Variáveis Essenciais:
```bash
SECRET_KEY=cole-aqui-chave-gerada
ENVIRONMENT=production
TINY_API_BASE_URL=https://api.tiny.com.br/api2
```

**Gerar SECRET_KEY**:
```powershell
# PowerShell
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString() + [System.Guid]::NewGuid().ToString()))
```

---

## ✅ Verificar Deploy

```bash
# 1. Health Check
curl https://SUA-URL.railway.app/health

# 2. Swagger
# Abra: https://SUA-URL.railway.app/docs

# 3. Criar Tenant
curl -X POST "https://SUA-URL.railway.app/api/v1/tenants" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Minha Empresa",
    "tiny_token": "SEU_TOKEN",
    "plano": "pro",
    "email_contato": "email@empresa.com"
  }'
```

---

## 🎉 Pronto!

Seu servidor está no ar com **120+ endpoints**!

**Documentação completa**: `GUIA_DEPLOY_COMPLETO.md`
**Exemplos de uso**: `EXEMPLOS_USO_NOVAS_FERRAMENTAS.md`
**Testes**: `RELATORIO_TESTES.md`

---

## 🆘 Problemas?

1. **Build falha**: Veja `railway logs --build`
2. **App não inicia**: Verifique variáveis de ambiente
3. **Erro 500**: Veja `railway logs`

**Guia completo de troubleshooting**: `GUIA_DEPLOY_COMPLETO.md` (Seção 🆘)
