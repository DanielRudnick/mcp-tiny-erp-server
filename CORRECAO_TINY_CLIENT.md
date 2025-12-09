# CORREÇÃO DO BUG NO tiny_client.py

## Problema Identificado

**Arquivo:** `src/services/tiny_client.py`
**Linhas:** 68-72

### Código ATUAL (com bug):
```python
async def incluir_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
    """Inclui novo pedido"""
    # API Tiny exige estrutura: {"pedido": {...}}
    pedido_wrapper = {"pedido": pedido}  # ❌ ERRO: Double wrapping!
    return await self._request("pedido.incluir", {"pedido": json.dumps(pedido_wrapper)})
```

### O que está acontecendo:
1. Recebe: `pedido = {"cliente": {...}, "itens": [...]}`
2. Cria wrapper: `pedido_wrapper = {"pedido": {...}}`
3. Serializa: `json.dumps({"pedido": {"cliente": {...}, "itens": [...]}})` ❌
4. Envia para API: `{"token": "...", "pedido": "{\"pedido\": {...}}"}`

### O que deveria acontecer:
1. Recebe: `pedido = {"cliente": {...}, "itens": [...]}`
2. Serializa direto: `json.dumps({"cliente": {...}, "itens": [...]})`
3. Envia para API: `{"token": "...", "pedido": "{\"cliente\": {...}, \"itens\": [...]}"}`

---

## SOLUÇÃO

### Código CORRIGIDO:
```python
async def incluir_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
    """Inclui novo pedido"""
    # A API Tiny espera: {"token": "...", "pedido": "<json_string>"}
    # Onde <json_string> já vem no formato correto do MCP tool
    return await self._request("pedido.incluir", {"pedido": json.dumps(pedido)})
```

---

## Por que isso importa?

De acordo com a documentação oficial da API Tiny:
https://tiny.com.br/api-docs/api2-pedidos-incluir

O payload HTTP deve ser:
```
POST /api2/pedido.incluir.php
Content-Type: application/x-www-form-urlencoded

token=SEU_TOKEN&pedido={"cliente":{"nome":"João"},"itens":[...]}&formato=json
```

Ou seja, o parâmetro `pedido` deve conter **diretamente** o JSON do pedido (como string), NÃO wrapped em `{"pedido": {...}}`.

---

## Outras correções similares necessárias:

Verifique se os mesmos métodos têm o mesmo bug:

### ✅ Métodos que parecem estar CORRETOS (sem double wrapping):
- `alterar_pedido` (linha 74-77) - ✅ OK
- `incluir_produto` (linha 108-116) - ✅ OK (usa estrutura diferente)
- `incluir_contato` (linha 167-175) - ✅ OK
- `incluir_nota_fiscal` (linha 217-225) - ✅ OK

### ⚠️ Métodos que podem ter problemas similares:
Revisar se há outros métodos `incluir_*` ou `alterar_*` que fazem wrapping desnecessário.

---

## Checklist de Aplicação:

- [ ] Parar o servidor (se estiver rodando)
- [ ] Abrir `src/services/tiny_client.py`
- [ ] Ir até a linha 68-72
- [ ] Remover a linha `pedido_wrapper = {"pedido": pedido}`
- [ ] Alterar `json.dumps(pedido_wrapper)` para `json.dumps(pedido)`
- [ ] Salvar o arquivo
- [ ] Fazer commit: `git add . && git commit -m "fix: remove double wrapping em incluir_pedido"`
- [ ] Fazer deploy (push + redeploy no Railway)
- [ ] Testar novamente no Sellflux

---

## Como testar se funcionou:

Após aplicar as correções, teste com este pedido mínimo:

```json
{
  "method": "tools/call",
  "params": {
    "name": "tiny_pedido_incluir",
    "arguments": {
      "pedido": {
        "cliente": {
          "nome": "Teste Cliente"
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
}
```

Se retornar sucesso (código do pedido criado), as correções funcionaram! 🎉
