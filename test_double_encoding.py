import httpx
import json

# Dados do pedido (EXATAMENTE como no log do Sellflux)
pedido_sellflux = {
    "itens": [{
        "item": {
            "codigo": "014000001",
            "unidade": "UN",
            "descricao": "Headset Wireless Gamer, Kalkan Ragnar, Sem Fio, RGB, 7.1 Surround Virtual, Preto - KLK025",
            "quantidade": "1",
            "valor_unitario": "294.97"
        }
    }],
    "cliente": {
        "fone": "41998251197",
        "nome": "Daniel Rudnick",
        "email": "d.rudnick.dr@gmail.com",
        "cidade": "São Caetano do Sul",
        "cpf_cnpj": "11283871904",
        "tipo_pessoa": "F"
    },
    "data_pedido": "28/11/2025"
}

# Testar preview direto
url = "https://mcp-tiny-erp-server-production.up.railway.app/test/pedido/preview"

response = httpx.post(url, json=pedido_sellflux, timeout=30)
result = response.json()

print("=== ANÁLISE DE SERIALIZAÇÃO ===\n")

print("1. PEDIDO ORIGINAL (Python dict):")
print(f"   Keys: {list(pedido_sellflux.keys())}")
print(f"   Cliente nome: {pedido_sellflux['cliente']['nome']}")
print(f"   Itens count: {len(pedido_sellflux['itens'])}")

print("\n2. SERIALIZADO (como vai para API Tiny):")
json_str = result["serializado_ascii_true"]
print(f"   Tamanho: {len(json_str)} chars")
print(f"   Começa com: {json_str[:100]}")

print("\n3. VALIDAÇÃO:")
for key, value in result["validacao"].items():
    print(f"   {key}: {value}")

print("\n4. PAYLOAD HTTP FINAL:")
payload = result["payload_que_seria_enviado"]
print(f"   token: {payload['token']}")
print(f"   formato: {payload['formato']}")
print(f"   pedido (primeiros 200 chars):")
print(f"   {payload['pedido'][:200]}...")

# Agora vamos fazer parse de volta para ver se a API Tiny conseguiria
print("\n5. TESTE DE PARSE (como a API Tiny faria):")
try:
    parsed_back = json.loads(payload['pedido'])
    print(f"   ✓ Parse OK!")
    print(f"   Cliente nome: {parsed_back.get('cliente', {}).get('nome')}")
    print(f"   Itens: {len(parsed_back.get('itens', []))}")
except Exception as e:
    print(f"   ✗ ERRO no parse: {e}")

