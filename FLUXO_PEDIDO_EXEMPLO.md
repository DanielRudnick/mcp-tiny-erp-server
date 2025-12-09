# 🔄 FLUXO COMPLETO: Criação de Pedido

## Exemplo Real do Sellflux

Baseado no teste que você fez:
- Cliente: Page Suprimentos de Informatica Ltda
- Produto: Cooler Air Clanm V19, 90mm, Preto
- Quantidade: 1
- Valor: R$ 44,97

---

## 📊 FLUXO PASSO A PASSO

### 1️⃣ USUÁRIO FAZ PEDIDO NO SELLFLUX
```
Usuário: "Quero comprar um Cooler Air Clanm V19"
```

### 2️⃣ AGENTE IA IDENTIFICA INTENÇÃO
```
Agente detecta:
- Ação: Criar pedido
- Produto: Cooler Air Clanm V19
- Cliente: Page Suprimentos (já cadastrado)
```

### 3️⃣ AGENTE MONTA CHAMADA MCP

**ANTES (com schema incompleto):** ❌
```json
{
  "method": "tools/call",
  "params": {
    "name": "tiny_pedido_incluir",
    "arguments": {}  // ❌ IA não sabe quais campos preencher!
  }
}
```

**DEPOIS (com schema corrigido):** ✅
```json
{
  "method": "tools/call",
  "params": {
    "name": "tiny_pedido_incluir",
    "arguments": {
      "pedido": {
        "data_pedido": "28/11/2025",
        "cliente": {
          "nome": "Page Suprimentos de Informatica Ltda",
          "tipo_pessoa": "J",
          "cpf_cnpj": "12345678000190",
          "email": "contato@pagesuprimentos.com.br"
        },
        "itens": [
          {
            "item": {
              "codigo": "COOLER-V19-BK",
              "descricao": "Cooler Air Clanm V19, 90mm, Preto",
              "unidade": "UN",
              "quantidade": "1",
              "valor_unitario": "44.97"
            }
          }
        ],
        "forma_pagamento": "boleto"
      }
    }
  }
}
```

### 4️⃣ SELLFLUX → MCP SERVER

**Request HTTP:**
```http
POST https://seu-servidor.railway.app/mcp
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "tiny_pedido_incluir",
    "arguments": {
      "pedido": { ... }
    }
  }
}
```

### 5️⃣ MCP SERVER VALIDA SCHEMA

**Schema Validation:**
```python
# mcp_server.py valida os argumentos contra o inputSchema
if validate_schema(arguments, tool.inputSchema):
    ✅ Schema válido! Prossegue...
else:
    ❌ "Received tool input did not match expected schema"
```

### 6️⃣ MCP EXECUTOR MAPEIA TOOL → METHOD

**mcp_executor.py:**
```python
# Busca mapeamento
tool_name = "tiny_pedido_incluir"
method_name = TOOL_METHOD_MAP[tool_name]  # → "incluir_pedido"

# Busca método no TinyAPIClient
method = getattr(client, method_name)  # → client.incluir_pedido

# Executa
result = await method(**arguments)  # → incluir_pedido(pedido={...})
```

### 7️⃣ TINY CLIENT PREPARA REQUISIÇÃO

**tiny_client.py:**

**ANTES (com double wrapping):** ❌
```python
# Recebe
pedido = {
  "data_pedido": "28/11/2025",
  "cliente": {...},
  "itens": [...]
}

# Faz wrapping ERRADO
pedido_wrapper = {"pedido": pedido}  # ❌

# Serializa
json_str = json.dumps(pedido_wrapper)
# Resultado: '{"pedido": {"data_pedido": "28/11/2025", ...}}'

# Envia para API
_request("pedido.incluir", {"pedido": json_str})
# API recebe: {"token": "...", "pedido": '{"pedido": {...}}'}  ❌❌
```

**DEPOIS (sem double wrapping):** ✅
```python
# Recebe
pedido = {
  "data_pedido": "28/11/2025",
  "cliente": {...},
  "itens": [...]
}

# Serializa DIRETO (sem wrapper extra)
json_str = json.dumps(pedido)
# Resultado: '{"data_pedido": "28/11/2025", "cliente": {...}, ...}'

# Envia para API
_request("pedido.incluir", {"pedido": json_str})
# API recebe: {"token": "...", "pedido": '{"data_pedido": "28/11/2025", ...}'}  ✅
```

### 8️⃣ REQUISIÇÃO HTTP PARA TINY ERP

**Request HTTP:**
```http
POST https://api.tiny.com.br/api2/pedido.incluir.php
Content-Type: application/x-www-form-urlencoded

token=SEU_TINY_TOKEN&formato=json&pedido={"data_pedido":"28/11/2025","cliente":{"nome":"Page Suprimentos de Informatica Ltda","tipo_pessoa":"J","cpf_cnpj":"12345678000190"},"itens":[{"item":{"codigo":"COOLER-V19-BK","descricao":"Cooler Air Clanm V19, 90mm, Preto","unidade":"UN","quantidade":"1","valor_unitario":"44.97"}}],"forma_pagamento":"boleto"}
```

### 9️⃣ API TINY PROCESSA

**Tiny ERP:**
1. Valida token ✅
2. Parse do JSON do pedido ✅
3. Valida campos obrigatórios ✅
4. Cria pedido no banco ✅
5. Retorna response

**Response da API Tiny:**
```json
{
  "retorno": {
    "status_processamento": "3",
    "status": "OK",
    "registros": [
      {
        "registro": {
          "sequencia": "1",
          "id": "789456123",
          "numero": "12345",
          "serie": "1",
          "data_pedido": "28/11/2025",
          "valor": "44.97"
        }
      }
    ]
  }
}
```

### 🔟 MCP SERVER → SELLFLUX

**Response MCP:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"retorno\":{\"status\":\"OK\",\"registros\":[{\"registro\":{\"id\":\"789456123\",\"numero\":\"12345\"}}]}}"
      }
    ]
  }
}
```

### 1️⃣1️⃣ AGENTE PROCESSA RESULTADO

```python
# Agente parseia a resposta
pedido_id = "789456123"
numero_pedido = "12345"

# Formata mensagem para usuário
mensagem = f"""
✅ Pedido criado com sucesso!

📝 Número: {numero_pedido}
🆔 ID: {pedido_id}
💰 Valor: R$ 44,97

Produto: Cooler Air Clanm V19, 90mm, Preto
Quantidade: 1

Você pode acompanhar seu pedido na área de clientes.
"""
```

### 1️⃣2️⃣ RESPOSTA PARA USUÁRIO

```
Agente: "✅ Pedido criado com sucesso!

📝 Número: 12345
🆔 ID: 789456123
💰 Valor: R$ 44,97

Produto: Cooler Air Clanm V19, 90mm, Preto
Quantidade: 1

Você pode acompanhar seu pedido na área de clientes."
```

---

## 📝 COMPARAÇÃO: ANTES vs DEPOIS

### ❌ ANTES DAS CORREÇÕES

```
Usuário → Agente → MCP (args: {}) → ❌ Schema Error
                                     ↓
                            "Received tool input did not match expected schema"
                                     ↓
                            Agente desiste após 3 tentativas
                                     ↓
                            "Desculpa, não consegui criar o pedido..."
```

### ✅ DEPOIS DAS CORREÇÕES

```
Usuário → Agente → MCP (args completos) → ✅ Schema OK
                                            ↓
                                   Executor mapeia tool
                                            ↓
                                   TinyClient prepara request
                                            ↓
                                   API Tiny processa
                                            ↓
                                   Pedido criado ✅
                                            ↓
                                   Response → Agente → Usuário
                                            ↓
                                   "✅ Pedido #12345 criado!"
```

---

## 🎯 PONTOS CRÍTICOS CORRIGIDOS

| Ponto | Antes | Depois |
|-------|-------|--------|
| **Schema cliente** | `{"type": "object"}` | Todas properties definidas |
| **Schema itens** | `{"type": "array"}` | Estrutura completa com "item" |
| **Campos obrigatórios** | Não especificados | `required: ["nome"]`, etc |
| **Wrapping pedido** | Double wrapping ❌ | Single wrapping ✅ |
| **Validação MCP** | Falha (args vazios) | Sucesso ✅ |
| **Request API Tiny** | Formato errado | Formato correto ✅ |

---

## 🧪 EXEMPLO DE TESTE CURL

Para testar a API direto (sem Sellflux):

```bash
# 1. Gerar JWT token (substitua SEU_TINY_TOKEN)
JWT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# 2. Testar criação de pedido
curl -X POST "https://seu-servidor.railway.app/mcp" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "tiny_pedido_incluir",
      "arguments": {
        "pedido": {
          "cliente": {
            "nome": "Cliente Teste"
          },
          "itens": [
            {
              "item": {
                "descricao": "Produto Teste",
                "unidade": "UN",
                "quantidade": "1",
                "valor_unitario": "10.00"
              }
            }
          ]
        }
      }
    }
  }'
```

Resposta esperada:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"retorno\":{\"status\":\"OK\",\"registros\":[{\"registro\":{\"id\":\"...\",\"numero\":\"...\"}}]}}"
      }
    ]
  }
}
```

---

**Referências:**
- Documentação API Tiny: https://tiny.com.br/api-docs/api2-pedidos-incluir
- MCP Protocol Spec: https://spec.modelcontextprotocol.io/
- JSON Schema: https://json-schema.org/
