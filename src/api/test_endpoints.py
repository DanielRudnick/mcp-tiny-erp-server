"""
Endpoints de teste para debug
"""
from fastapi import APIRouter, Body
from typing import Dict, Any
import json

router = APIRouter(prefix="/test", tags=["🧪 Debug & Test"])


@router.post("/pedido/preview", summary="Preview do pedido que seria enviado à API Tiny")
async def preview_pedido(pedido: Dict[str, Any] = Body(...)):
    """
    Mostra exatamente o JSON que seria enviado para a API Tiny
    sem fazer a chamada real.

    Use este endpoint para debug!
    """

    # Serializar exatamente como o código faz
    pedido_json_ascii_true = json.dumps(pedido, ensure_ascii=True, separators=(',', ':'))
    pedido_json_ascii_false = json.dumps(pedido, ensure_ascii=False, separators=(',', ':'))
    pedido_json_formatted = json.dumps(pedido, indent=2, ensure_ascii=False)

    return {
        "status": "preview",
        "input_recebido": pedido,
        "serializado_ascii_true": pedido_json_ascii_true,
        "serializado_ascii_false": pedido_json_ascii_false,
        "formatado_legivel": pedido_json_formatted,
        "tamanho_bytes_ascii_true": len(pedido_json_ascii_true.encode('utf-8')),
        "tamanho_bytes_ascii_false": len(pedido_json_ascii_false.encode('utf-8')),
        "validacao": {
            "tem_cliente": "cliente" in pedido,
            "tem_nome_cliente": pedido.get("cliente", {}).get("nome") if isinstance(pedido.get("cliente"), dict) else None,
            "tem_itens": "itens" in pedido,
            "qtd_itens": len(pedido.get("itens", [])) if isinstance(pedido.get("itens"), list) else 0,
            "primeiro_item": pedido.get("itens", [{}])[0] if pedido.get("itens") else None
        },
        "payload_que_seria_enviado": {
            "token": "***HIDDEN***",
            "formato": "JSON",
            "pedido": pedido_json_ascii_true
        },
        "info": "Este é o payload exato que seria enviado para https://api.tiny.com.br/api2/pedido.incluir.php"
    }


@router.post("/mcp/simulate-call", summary="Simula chamada MCP para tiny_pedido_incluir")
async def simulate_mcp_call(arguments: Dict[str, Any] = Body(...)):
    """
    Simula exatamente o fluxo MCP → TinyClient

    Envie no formato:
    {
      "pedido": {
        "cliente": {"nome": "Teste"},
        "itens": [{"item": {...}}]
      }
    }
    """

    # Extrair pedido como o mcp_server.py faz
    pedido_data = arguments.get("pedido")

    if not pedido_data:
        return {
            "erro": "Argumento 'pedido' não encontrado!",
            "arguments_recebidos": arguments,
            "keys_disponiveis": list(arguments.keys()) if isinstance(arguments, dict) else None
        }

    # Serializar como tiny_client.py faz
    pedido_json = json.dumps(pedido_data, ensure_ascii=True, separators=(',', ':'))

    return {
        "status": "simulacao_mcp_ok",
        "fluxo": {
            "1_arguments_mcp": arguments,
            "2_pedido_extraido": pedido_data,
            "3_pedido_serializado": pedido_json,
            "4_payload_final": {
                "token": "***HIDDEN***",
                "formato": "JSON",
                "pedido": pedido_json
            }
        },
        "validacao": {
            "pedido_data_tipo": str(type(pedido_data)),
            "tem_cliente": "cliente" in pedido_data if isinstance(pedido_data, dict) else False,
            "tem_itens": "itens" in pedido_data if isinstance(pedido_data, dict) else False,
            "nome_cliente": pedido_data.get("cliente", {}).get("nome") if isinstance(pedido_data, dict) else None
        }
    }


@router.get("/health", summary="Health check do módulo de testes")
async def test_health():
    """Health check"""
    return {"status": "ok", "module": "test_endpoints"}
