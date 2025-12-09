# 🔧 GUIA COMPLETO: Corrigir Tool tiny_pedido_incluir

## 📋 Resumo do Problema

Analisando os logs do Sellflux, identificamos **2 problemas críticos**:

### 1. ❌ Schema Incompleto (PRINCIPAL)
**Arquivo:** `src/api/mcp_tools.py` (linhas 53-71)

A IA não consegue gerar argumentos porque o `inputSchema` não define:
- Quais campos tem dentro de `cliente`
- Qual a estrutura dos itens no array `itens`
- Quais campos são obrigatórios

**Resultado:** IA envia `args: {}` vazio → Erro "Received tool input did not match expected schema"

### 2. ❌ Bug de Double Wrapping
**Arquivo:** `src/services/tiny_client.py` (linhas 68-72)

O código faz wrapping duplo do objeto pedido antes de enviar para a API Tiny:
```python
pedido_wrapper = {"pedido": pedido}  # ❌ Wrapping desnecessário
```

**Resultado:** API Tiny recebe `{"pedido": {"pedido": {...}}}` ao invés de `{"pedido": {...}}`

---

## 🛠️ CORREÇÕES NECESSÁRIAS

### CORREÇÃO 1: Atualizar Schema Completo

**Arquivo:** `src/api/mcp_tools.py`
**Localização:** Linhas 53-71
**Ação:** Substituir a tool `tiny_pedido_incluir` pelo código do arquivo `CORRECAO_SCHEMA_PEDIDO.py`

#### O que muda:
- ✅ Define TODAS as properties de `cliente` (nome, cpf_cnpj, email, etc)
- ✅ Define estrutura completa dos `itens` incluindo o wrapper `item`
- ✅ Marca campos obrigatórios vs opcionais
- ✅ Adiciona descrições detalhadas para cada campo
- ✅ Define tipos corretos (string, object, array)

---

### CORREÇÃO 2: Remover Double Wrapping

**Arquivo:** `src/services/tiny_client.py`
**Localização:** Linhas 68-72

#### ANTES (com bug):
```python
async def incluir_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
    """Inclui novo pedido"""
    # API Tiny exige estrutura: {"pedido": {...}}
    pedido_wrapper = {"pedido": pedido}
    return await self._request("pedido.incluir", {"pedido": json.dumps(pedido_wrapper)})
```

#### DEPOIS (corrigido):
```python
async def incluir_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
    """Inclui novo pedido"""
    # A API Tiny espera receber o objeto pedido serializado diretamente
    return await self._request("pedido.incluir", {"pedido": json.dumps(pedido)})
```

#### Como aplicar:
1. Abrir `src/services/tiny_client.py`
2. Ir até linha 68-72
3. Deletar a linha: `pedido_wrapper = {"pedido": pedido}`
4. Alterar `json.dumps(pedido_wrapper)` para `json.dumps(pedido)`
5. Salvar

---

## 📝 PASSO A PASSO COMPLETO

### 1. Preparar Ambiente
```bash
cd ~/Downloads/mcp-tiny-erp-server

# Verificar status atual
git status

# Criar branch para correções
git checkout -b fix/pedido-incluir-schema
```

### 2. Aplicar Correção 1 - Schema

Abrir no editor: `src/api/mcp_tools.py`

Localizar as linhas 53-71 (tool `tiny_pedido_incluir`)

Substituir TODO o bloco `Tool(...)` pelo conteúdo de `CORRECAO_SCHEMA_PEDIDO.py`

Salvar o arquivo.

### 3. Aplicar Correção 2 - Double Wrapping

Abrir no editor: `src/services/tiny_client.py`

Localizar método `incluir_pedido` (linha ~68)

Fazer as alterações conforme descrito acima.

Salvar o arquivo.

### 4. Testar Localmente (Opcional)
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python -m uvicorn src.main:app --reload

# Em outro terminal, testar
curl http://localhost:8000/health
```

### 5. Commit e Deploy
```bash
# Adicionar mudanças
git add src/api/mcp_tools.py src/services/tiny_client.py

# Commit
git commit -m "fix: corrigir schema e double wrapping em tiny_pedido_incluir

- Adiciona schema JSON completo para tool tiny_pedido_incluir
- Define todas as properties de cliente e itens
- Remove double wrapping no método incluir_pedido
- Corrige estrutura de dados enviada para API Tiny"

# Push para GitHub
git push origin fix/pedido-incluir-schema

# Fazer merge na main
git checkout main
git merge fix/pedido-incluir-schema
git push origin main
```

### 6. Deploy no Railway

Opção A - Deploy Automático:
- Railway detecta o push e faz deploy automaticamente (~2-3 min)
- Acompanhe em: https://railway.app/project/seu-projeto

Opção B - Deploy Manual:
1. Acesse Railway Dashboard
2. Vá no projeto MCP Tiny ERP Server
3. Clique em "Deployments"
4. Clique em "Deploy Now"

### 7. Verificar Deploy

Aguardar deploy finalizar e testar:
```bash
# Verificar health
curl https://SEU-SERVIDOR.railway.app/health

# Verificar ferramentas MCP
curl https://SEU-SERVIDOR.railway.app/mcp/info
```

---

## 🧪 TESTE COMPLETO NO SELLFLUX

### Teste 1: Pedido Mínimo
Peça ao agente:
> "Cria um pedido de teste com cliente 'João Silva' e produto 'Teste', 1 unidade, R$ 10,00"

Deve funcionar e retornar ID do pedido criado.

### Teste 2: Pedido Completo (Caso Real)
Peça ao agente:
> "Cria um pedido para Page Suprimentos, CNPJ 12345678000190, produto Cooler Air Clanm V19 90mm Preto, 1 unidade, R$ 44,97"

Deve funcionar e criar o pedido com todos os dados.

### Teste 3: Verificar no Tiny ERP
1. Acesse https://tiny.com.br
2. Vá em Pedidos
3. Verifique se os pedidos de teste foram criados
4. Confira se todos os dados estão corretos

---

## ✅ CHECKLIST DE VERIFICAÇÃO

- [ ] Schema atualizado em `mcp_tools.py`
- [ ] Double wrapping removido em `tiny_client.py`
- [ ] Código testado localmente
- [ ] Commit realizado
- [ ] Push para GitHub
- [ ] Deploy no Railway concluído
- [ ] Health check OK
- [ ] Teste mínimo no Sellflux funcionou
- [ ] Teste completo no Sellflux funcionou
- [ ] Pedidos aparecem no Tiny ERP
- [ ] Dados do pedido estão corretos

---

## 🐛 TROUBLESHOOTING

### Problema: IA ainda envia args vazios
**Causa:** Schema não foi atualizado corretamente
**Solução:**
1. Verificar se o arquivo foi salvo
2. Verificar se fez deploy
3. Reiniciar conexão MCP no Sellflux

### Problema: Erro 500 ao criar pedido
**Causa:** Bug do double wrapping ainda presente
**Solução:**
1. Verificar se removeu a linha `pedido_wrapper`
2. Verificar se alterou `json.dumps(pedido)`
3. Fazer deploy novamente

### Problema: API Tiny retorna erro de campos obrigatórios
**Causa:** Estrutura do pedido incorreta
**Solução:**
1. Verificar logs da API Tiny
2. Conferir se itens estão dentro de `{"item": {...}}`
3. Verificar se `cliente.nome` está presente

### Problema: Deploy no Railway falhou
**Causa:** Erro de sintaxe Python
**Solução:**
1. Verificar logs do Railway
2. Testar localmente: `python -m py_compile src/api/mcp_tools.py`
3. Corrigir erros de sintaxe e fazer novo commit

---

## 📞 PRECISA DE AJUDA?

Se mesmo após aplicar as correções o problema persistir:

1. Colete os logs do Sellflux (igual você fez)
2. Colete os logs do Railway (Deploy > View Logs)
3. Teste a API direto com curl/Postman
4. Me mande os logs para análise

---

## 🎯 RESULTADO ESPERADO

Após aplicar as correções:

✅ IA consegue gerar argumentos corretos
✅ Schema validação passa
✅ Pedido é enviado para API Tiny no formato correto
✅ Pedido é criado com sucesso no Tiny ERP
✅ Agente responde com ID do pedido criado

---

**Criado em:** 28/11/2025
**Versão:** 1.0
**Status:** Pronto para aplicação
