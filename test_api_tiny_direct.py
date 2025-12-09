import httpx
import json

# Teste direto da API Tiny
async def test_tiny_api():
    # Pedido minimo
    pedido = {
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
    
    # Serializar JSON
    pedido_json = json.dumps(pedido, ensure_ascii=False, separators=(',', ':'))
    
    print(f"JSON que sera enviado:")
    print(pedido_json)
    print(f"\nTamanho: {len(pedido_json)} chars")
    print(f"\nJSON formatado:")
    print(json.dumps(pedido, indent=2, ensure_ascii=False))
    
    # Preparar payload
    payload = {
        "token": "SEU_TOKEN_AQUI",  # Substituir com token real
        "formato": "JSON",
        "pedido": pedido_json
    }
    
    print(f"\n\nPayload completo:")
    for key, value in payload.items():
        if key == "pedido":
            print(f"{key}: {value[:100]}...")
        else:
            print(f"{key}: {value}")
    
    # Comentar a linha abaixo para nao fazer request real
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         "https://api.tiny.com.br/api2/pedido.incluir.php",
    #         data=payload
    #     )
    #     print(f"\n\nResponse: {response.status_code}")
    #     print(response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_tiny_api())

