# Script de Deploy para MCP Tiny ERP Server (PowerShell)
# Uso: .\deploy.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOY - MCP TINY ERP SERVER" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Função para printar com cor
function Print-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Print-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Print-Info {
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

# Verifica se está no diretório correto
if (-not (Test-Path "requirements.txt")) {
    Print-Error "Execute este script no diretório raiz do projeto!"
    exit 1
}

Print-Success "Diretório correto verificado"

# Verifica se git está inicializado
if (-not (Test-Path ".git")) {
    Print-Error "Repositório git não inicializado!"
    Print-Info "Execute: git init"
    exit 1
}

Print-Success "Repositório git encontrado"

# Adiciona novos arquivos
Write-Host ""
Print-Info "Adicionando novos arquivos ao git..."

try {
    git add src/api/mcp_tools_completo.py
    git add src/services/tiny_client.py
    git add NOVO_MCP_TOOLS_COMPLETO.md
    git add EXEMPLOS_USO_NOVAS_FERRAMENTAS.md
    git add RELATORIO_TESTES.md
    git add test_novas_ferramentas.py
    git add GUIA_DEPLOY_COMPLETO.md
    git add deploy.sh
    git add deploy.ps1

    Print-Success "Arquivos adicionados"
} catch {
    Print-Error "Erro ao adicionar arquivos"
    exit 1
}

# Verifica status
Write-Host ""
Print-Info "Status do repositório:"
git status --short

# Commit
Write-Host ""
$commit = Read-Host "📝 Deseja fazer commit? (y/n)"
if ($commit -eq "y" -or $commit -eq "Y") {
    $commitMessage = @"
feat: adicionar 120+ novos endpoints da API Tiny

- Implementados todos os endpoints da API Tiny V2
- Adicionados métodos para: Contatos, Produtos, CRM, Contas, Notas Fiscais, PDV, Expedições, etc
- Sistema de cache e rate limiting implementado
- Documentação completa e exemplos de uso
- Testes de validação criados
- 100% de cobertura da API Tiny
- Scripts de deploy automatizados
"@

    git commit -m $commitMessage
    Print-Success "Commit realizado"
}

# Push
Write-Host ""
$push = Read-Host "🚀 Deseja fazer push para o GitHub? (y/n)"
if ($push -eq "y" -or $push -eq "Y") {
    $branch = git rev-parse --abbrev-ref HEAD
    git push origin $branch
    Print-Success "Push realizado para branch: $branch"
}

# Informações
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ PRÓXIMOS PASSOS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  Acesse Railway: https://railway.app"
Write-Host "2️⃣  Crie novo projeto: 'New Project' → 'Deploy from GitHub'"
Write-Host "3️⃣  Selecione: mcp-tiny-erp-server"
Write-Host "4️⃣  Adicione PostgreSQL: 'New' → 'Database' → 'PostgreSQL'"
Write-Host "5️⃣  Adicione Redis: 'New' → 'Database' → 'Redis'"
Write-Host "6️⃣  Configure variáveis (veja GUIA_DEPLOY_COMPLETO.md)"
Write-Host "7️⃣  Aguarde deploy (3-5 minutos)"
Write-Host ""
Write-Host "📖 Guia completo: GUIA_DEPLOY_COMPLETO.md"
Write-Host "📊 Relatório de testes: RELATORIO_TESTES.md"
Write-Host "📚 Exemplos de uso: EXEMPLOS_USO_NOVAS_FERRAMENTAS.md"
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Print-Success "Script concluído com sucesso!"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 DICA: Para gerar SECRET_KEY, execute:" -ForegroundColor Yellow
Write-Host "   [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString() + [System.Guid]::NewGuid().ToString()))" -ForegroundColor Gray
