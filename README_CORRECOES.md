# 🚨 CORREÇÕES URGENTES - tiny_pedido_incluir

## ⚡ TL;DR - Aplicação Rápida (5 minutos)

### 1. Parar servidor (se rodando)

### 2. Editar `src/api/mcp_tools.py` (linhas 53-71)
Substituir a tool `tiny_pedido_incluir` pelo código de: **`CORRECAO_SCHEMA_PEDIDO.py`**

### 3. Editar `src/services/tiny_client.py` (linha ~70)
```python
# DELETAR esta linha:
pedido_wrapper = {"pedido": pedido}

# ALTERAR de:
return await self._request("pedido.incluir", {"pedido": json.dumps(pedido_wrapper)})

# PARA:
return await self._request("pedido.incluir", {"pedido": json.dumps(pedido)})
```

### 4. Commit e Deploy
```bash
git add src/api/mcp_tools.py src/services/tiny_client.py
git commit -m "fix: corrigir schema e double wrapping em tiny_pedido_incluir"
git push origin main
```

### 5. Aguardar deploy Railway (~2-3 min)

### 6. Testar no Sellflux
```
"Cria um pedido de teste com cliente João Silva, produto Teste, R$ 10"
```

Deve funcionar! ✅

---

## 📚 Documentação Completa

Acesse os arquivos para detalhes:

| Arquivo | Conteúdo |
|---------|----------|
| **GUIA_CORRECAO_COMPLETO.md** | 📖 Passo a passo detalhado + troubleshooting |
| **CORRECAO_SCHEMA_PEDIDO.py** | 💻 Código Python do schema corrigido |
| **CORRECAO_TINY_CLIENT.md** | 🐛 Explicação do bug double wrapping |
| **FLUXO_PEDIDO_EXEMPLO.md** | 🔄 Fluxo visual completo do pedido |

---

## 🎯 O que foi corrigido?

### Problema 1: Schema Incompleto ❌
```python
# ANTES
"cliente": {"type": "object"}  # IA não sabe quais campos!
"itens": {"type": "array"}      # IA não sabe a estrutura!

# DEPOIS ✅
"cliente": {
  "properties": {
    "nome": {"type": "string", "description": "..."},
    "cpf_cnpj": {"type": "string", "description": "..."},
    ...
  },
  "required": ["nome"]
}
```

### Problema 2: Double Wrapping ❌
```python
# ANTES
pedido_wrapper = {"pedido": pedido}  # Wrapping extra!
json.dumps(pedido_wrapper)           # {"pedido": {"pedido": {...}}}

# DEPOIS ✅
json.dumps(pedido)  # {"pedido": {...}}
```

---

## ✅ Checklist Rápido

- [ ] Schema atualizado
- [ ] Double wrapping removido
- [ ] Código commitado
- [ ] Deploy realizado
- [ ] Teste no Sellflux OK

---

## 🆘 Problemas?

1. **IA ainda envia args vazios**
   → Verificar se schema foi atualizado e deploy feito

2. **Erro 500 ao criar pedido**
   → Verificar se removeu linha `pedido_wrapper`

3. **Deploy falhou**
   → Verificar logs Railway e sintaxe Python

---

**Criado:** 28/11/2025
**Status:** ✅ Pronto para aplicação
**Tempo estimado:** 5-10 minutos
