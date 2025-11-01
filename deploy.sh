#!/bin/bash

# Script de Deploy para MCP Tiny ERP Server
# Uso: ./deploy.sh

set -e

echo "=========================================="
echo "🚀 DEPLOY - MCP TINY ERP SERVER"
echo "=========================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para printar com cor
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Verifica se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    print_error "Execute este script no diretório raiz do projeto!"
    exit 1
fi

print_success "Diretório correto verificado"

# Verifica se git está inicializado
if [ ! -d ".git" ]; then
    print_error "Repositório git não inicializado!"
    print_info "Execute: git init"
    exit 1
fi

print_success "Repositório git encontrado"

# Adiciona novos arquivos
echo ""
print_info "Adicionando novos arquivos ao git..."

git add src/api/mcp_tools_completo.py
git add src/services/tiny_client.py
git add NOVO_MCP_TOOLS_COMPLETO.md
git add EXEMPLOS_USO_NOVAS_FERRAMENTAS.md
git add RELATORIO_TESTES.md
git add test_novas_ferramentas.py
git add GUIA_DEPLOY_COMPLETO.md
git add deploy.sh
git add deploy.ps1

print_success "Arquivos adicionados"

# Verifica status
echo ""
print_info "Status do repositório:"
git status --short

# Commit
echo ""
read -p "📝 Deseja fazer commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git commit -m "feat: adicionar 120+ novos endpoints da API Tiny

- Implementados todos os endpoints da API Tiny V2
- Adicionados métodos para: Contatos, Produtos, CRM, Contas, Notas Fiscais, PDV, Expedições, etc
- Sistema de cache e rate limiting implementado
- Documentação completa e exemplos de uso
- Testes de validação criados
- 100% de cobertura da API Tiny
- Scripts de deploy automatizados"

    print_success "Commit realizado"
fi

# Push
echo ""
read -p "🚀 Deseja fazer push para o GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    git push origin $BRANCH
    print_success "Push realizado para branch: $BRANCH"
fi

# Informações
echo ""
echo "=========================================="
echo "✅ PRÓXIMOS PASSOS"
echo "=========================================="
echo ""
echo "1️⃣  Acesse Railway: https://railway.app"
echo "2️⃣  Crie novo projeto: 'New Project' → 'Deploy from GitHub'"
echo "3️⃣  Selecione: mcp-tiny-erp-server"
echo "4️⃣  Adicione PostgreSQL: 'New' → 'Database' → 'PostgreSQL'"
echo "5️⃣  Adicione Redis: 'New' → 'Database' → 'Redis'"
echo "6️⃣  Configure variáveis (veja GUIA_DEPLOY_COMPLETO.md)"
echo "7️⃣  Aguarde deploy (3-5 minutos)"
echo ""
echo "📖 Guia completo: GUIA_DEPLOY_COMPLETO.md"
echo "📊 Relatório de testes: RELATORIO_TESTES.md"
echo "📚 Exemplos de uso: EXEMPLOS_USO_NOVAS_FERRAMENTAS.md"
echo ""
echo "=========================================="
print_success "Script concluído com sucesso!"
echo "=========================================="
