"""
MCP Server - Model Context Protocol 2025-06-18 Implementation
Servidor completo com 68+ ferramentas para integração Tiny ERP
"""

from fastapi import APIRouter, Request, Response, HTTPException, Header
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
import json
import asyncio
import uuid
import base64

# Imports do projeto
from src.services.tiny_client import TinyAPIClient
from src.api.mcp_tools import get_all_tools, get_tool_by_name, get_tools_count

router = APIRouter(tags=["MCP Protocol"])

# =============================================================================
# PROTOCOL VERSION
# =============================================================================

MCP_PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"]

# =============================================================================
# AUTHENTICATION
# =============================================================================

async def get_auth_data(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Extrai dados de autenticação do JWT token.
    Pega tiny_token direto do JWT.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization required")

    token = authorization.replace("Bearer ", "").strip()

    # Decodifica JWT manualmente (sem validação de assinatura)
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        # Decodifica payload (segunda parte do JWT)
        payload_encoded = parts[1]
        padding = 4 - (len(payload_encoded) % 4)
        if padding != 4:
            payload_encoded += "=" * padding

        payload_json = base64.urlsafe_b64decode(payload_encoded)
        payload = json.loads(payload_json)

        # Extrai dados do JWT
        tenant_id = payload.get("tenant_id") or payload.get("sub")
        tiny_token = payload.get("tiny_token")

        if not tenant_id:
            raise HTTPException(status_code=401, detail="Token inválido: falta tenant_id")

        if not tiny_token:
            raise HTTPException(
                status_code=401,
                detail="Token inválido: falta tiny_token. Faça login novamente."
            )

        return {
            "tenant_id": tenant_id,
            "tiny_token": tiny_token,
            "tenant_nome": payload.get("tenant_nome", ""),
            "plano": payload.get("plano", "free")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro ao processar token: {str(e)}")


# =============================================================================
# MODELS
# =============================================================================

class ServerInfo(BaseModel):
    name: str
    version: str


class ServerCapabilities(BaseModel):
    tools: Optional[Dict[str, Any]] = None
    resources: Optional[Dict[str, Any]] = None
    prompts: Optional[Dict[str, Any]] = None


# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

class MCPSession:
    """Gerencia sessão MCP por cliente"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.initialized = False
        self.tenant_id = None
        self.tiny_token = None
        self.created_at = datetime.utcnow()


sessions: Dict[str, MCPSession] = {}


# =============================================================================
# CAPABILITIES
# =============================================================================

def get_server_capabilities() -> ServerCapabilities:
    return ServerCapabilities(
        tools={"listChanged": False},
        resources={"subscribe": False, "listChanged": False},
        prompts={"listChanged": False}
    )


def get_server_info() -> ServerInfo:
    return ServerInfo(
        name="mcp-tiny-erp-server",
        version="2.0.0"
    )


# =============================================================================
# JSON-RPC HANDLER
# =============================================================================

async def handle_jsonrpc_request(
    data: Dict[str, Any],
    session: MCPSession
) -> Optional[Dict[str, Any]]:
    """Processa requisição JSON-RPC 2.0"""

    try:
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id")

        # Notification (sem resposta)
        if request_id is None:
            if method == "notifications/initialized":
                session.initialized = True
            return None

        # Roteamento de métodos
        if method == "initialize":
            result = {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": get_server_capabilities().model_dump(exclude_none=True),
                "serverInfo": get_server_info().model_dump(),
                "instructions": f"Servidor MCP Tiny ERP com {get_tools_count()} ferramentas disponíveis"
            }

        elif method == "tools/list":
            # Auto-initialize se não foi inicializado (compatibilidade com Sellflux)
            if not session.initialized:
                session.initialized = True

            tools = get_all_tools()
            result = {"tools": [t.model_dump() for t in tools]}

        elif method == "tools/call":
            # Auto-initialize se não foi inicializado (compatibilidade com Sellflux)
            if not session.initialized:
                session.initialized = True

            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            tiny_client = TinyAPIClient(token=session.tiny_token)
            tool_result = await execute_tiny_tool(tiny_client, tool_name, arguments)

            result = {
                "content": [{
                    "type": "text",
                    "text": json.dumps(tool_result, ensure_ascii=False, indent=2)
                }]
            }

        elif method == "ping":
            result = {}

        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": data.get("id"),
            "error": {"code": -32603, "message": str(e)}
        }


# =============================================================================
# TOOL EXECUTION
# =============================================================================

async def execute_tiny_tool(
    client: TinyAPIClient,
    tool_name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """Executa uma ferramenta do Tiny ERP - MAPEAMENTO COMPLETO"""

    # PEDIDOS
    if tool_name == "tiny_pedidos_pesquisar":
        return await client.pesquisar_pedidos(**arguments)
    elif tool_name == "tiny_pedido_obter":
        return await client.obter_pedido(arguments.get("id"))
    elif tool_name == "tiny_pedido_incluir":
        pedido_data = arguments.get("pedido")
        print(f"[DEBUG MCP] Recebido pedido: {str(pedido_data)[:200]}...")
        print(f"[DEBUG MCP] Tipo: {type(pedido_data)}")
        if pedido_data:
            print(f"[DEBUG MCP] Keys: {pedido_data.keys() if isinstance(pedido_data, dict) else 'N/A'}")
        return await client.incluir_pedido(pedido_data)
    elif tool_name == "tiny_pedido_alterar":
        return await client.alterar_pedido(arguments.get("id"), arguments.get("pedido"))
    elif tool_name == "tiny_pedido_alterar_situacao":
        return await client.alterar_situacao_pedido(arguments.get("id"), arguments.get("situacao"))
    elif tool_name == "tiny_pedido_obter_rastreamento":
        return await client.obter_rastreamento_pedido(arguments.get("id"))

    # PRODUTOS
    elif tool_name == "tiny_produtos_pesquisar":
        return await client.pesquisar_produtos(**arguments)
    elif tool_name == "tiny_produto_obter":
        return await client.obter_produto(arguments.get("id"))
    elif tool_name == "tiny_produto_incluir":
        return await client.incluir_produto(arguments.get("produto"))
    elif tool_name == "tiny_produto_alterar":
        return await client.alterar_produto(arguments.get("id"), arguments.get("produto"))
    elif tool_name == "tiny_produto_obter_estoque":
        return await client.obter_estoque_produto(arguments.get("id"))
    elif tool_name == "tiny_produto_atualizar_estoque":
        return await client.atualizar_estoque_produto(arguments.get("id"), arguments.get("estoque"))
    elif tool_name == "tiny_produto_obter_preco":
        return await client.obter_preco_produto(arguments.get("id"))

    # CONTATOS
    elif tool_name == "tiny_contatos_pesquisar":
        return await client.pesquisar_contatos(**arguments)
    elif tool_name == "tiny_contato_obter":
        return await client.obter_contato(arguments.get("id"))
    elif tool_name == "tiny_contato_incluir":
        return await client.incluir_contato(arguments.get("contato"))
    elif tool_name == "tiny_contato_alterar":
        return await client.alterar_contato(arguments.get("id"), arguments.get("contato"))

    # NOTAS FISCAIS
    elif tool_name == "tiny_notas_fiscais_pesquisar":
        return await client.pesquisar_notas_fiscais(**arguments)
    elif tool_name == "tiny_nota_fiscal_obter":
        return await client.obter_nota_fiscal(arguments.get("id"))
    elif tool_name == "tiny_nota_fiscal_incluir":
        return await client.incluir_nota_fiscal(arguments.get("nota"))
    elif tool_name == "tiny_nota_fiscal_gerar_pedido":
        return await client.gerar_nota_fiscal_pedido(arguments.get("pedido_id"))
    elif tool_name == "tiny_nota_fiscal_enviar_email":
        return await client.enviar_email_nota_fiscal(arguments.get("id"), arguments.get("email"))
    elif tool_name == "tiny_nota_fiscal_obter_xml":
        return await client.obter_xml_nota_fiscal(arguments.get("id"))
    elif tool_name == "tiny_nota_fiscal_cancelar":
        return await client.cancelar_nota_fiscal(arguments.get("id"), arguments.get("motivo"))

    # CONTAS A RECEBER
    elif tool_name == "tiny_contas_receber_pesquisar":
        return await client.pesquisar_contas_receber(**arguments)
    elif tool_name == "tiny_conta_receber_obter":
        return await client.obter_conta_receber(arguments.get("id"))
    elif tool_name == "tiny_conta_receber_incluir":
        return await client.incluir_conta_receber(arguments.get("conta"))
    elif tool_name == "tiny_conta_receber_baixar":
        return await client.baixar_conta_receber(
            arguments.get("id"),
            arguments.get("data_pagamento"),
            arguments.get("valor")
        )

    # CONTAS A PAGAR
    elif tool_name == "tiny_contas_pagar_pesquisar":
        return await client.pesquisar_contas_pagar(**arguments)
    elif tool_name == "tiny_conta_pagar_obter":
        return await client.obter_conta_pagar(arguments.get("id"))
    elif tool_name == "tiny_conta_pagar_incluir":
        return await client.incluir_conta_pagar(arguments.get("conta"))
    elif tool_name == "tiny_conta_pagar_baixar":
        return await client.baixar_conta_pagar(
            arguments.get("id"),
            arguments.get("data_pagamento"),
            arguments.get("valor")
        )

    # CRM
    elif tool_name == "tiny_crm_oportunidades_pesquisar":
        return await client.pesquisar_oportunidades_crm(arguments.get("pagina", 1))
    elif tool_name == "tiny_crm_oportunidade_obter":
        return await client.obter_oportunidade_crm(arguments.get("id"))
    elif tool_name == "tiny_crm_oportunidade_incluir":
        return await client.incluir_oportunidade_crm(arguments.get("oportunidade"))
    elif tool_name == "tiny_crm_oportunidade_alterar":
        return await client.alterar_oportunidade_crm(arguments.get("id"), arguments.get("oportunidade"))

    # COMPLEMENTARES
    elif tool_name == "tiny_formas_pagamento_listar":
        return await client.listar_formas_pagamento()
    elif tool_name == "tiny_transportadoras_pesquisar":
        return await client.pesquisar_transportadoras(arguments.get("pagina", 1))
    elif tool_name == "tiny_transportadora_obter":
        return await client.obter_transportadora(arguments.get("id"))
    elif tool_name == "tiny_vendedores_pesquisar":
        return await client.pesquisar_vendedores(arguments.get("pagina", 1))
    elif tool_name == "tiny_vendedor_obter":
        return await client.obter_vendedor(arguments.get("id"))
    elif tool_name == "tiny_categorias_listar":
        return await client.listar_categorias()
    elif tool_name == "tiny_etiquetas_listar":
        return await client.listar_etiquetas()
    elif tool_name == "tiny_depositos_listar":
        return await client.listar_depositos()
    elif tool_name == "tiny_deposito_obter_estoque":
        return await client.obter_estoque_deposito(arguments.get("id"))
    elif tool_name == "tiny_orcamentos_pesquisar":
        return await client.pesquisar_orcamentos(**arguments)
    elif tool_name == "tiny_orcamento_obter":
        return await client.obter_orcamento(arguments.get("id"))
    elif tool_name == "tiny_orcamento_incluir":
        return await client.incluir_orcamento(arguments.get("orcamento"))
    elif tool_name == "tiny_pedidos_compra_pesquisar":
        return await client.pesquisar_pedidos_compra(arguments.get("pagina", 1))
    elif tool_name == "tiny_pedido_compra_obter":
        return await client.obter_pedido_compra(arguments.get("id"))
    elif tool_name == "tiny_pedido_compra_incluir":
        return await client.incluir_pedido_compra(arguments.get("pedido"))
    elif tool_name == "tiny_manifestos_pesquisar":
        return await client.pesquisar_manifestos(arguments.get("pagina", 1))
    elif tool_name == "tiny_manifesto_obter":
        return await client.obter_manifesto(arguments.get("id"))
    elif tool_name == "tiny_ordens_servico_pesquisar":
        return await client.pesquisar_ordens_servico(arguments.get("pagina", 1))
    elif tool_name == "tiny_ordem_servico_obter":
        return await client.obter_ordem_servico(arguments.get("id"))
    elif tool_name == "tiny_kits_pesquisar":
        return await client.pesquisar_kits(arguments.get("pagina", 1))
    elif tool_name == "tiny_kit_obter":
        return await client.obter_kit(arguments.get("id"))
    elif tool_name == "tiny_expedicoes_pesquisar":
        return await client.pesquisar_expedicoes(arguments.get("pagina", 1))
    elif tool_name == "tiny_expedicao_obter":
        return await client.obter_expedicao(arguments.get("id"))
    elif tool_name == "tiny_pdv_vendas_pesquisar":
        return await client.pesquisar_vendas_pdv(arguments.get("pagina", 1))
    elif tool_name == "tiny_pdv_venda_obter":
        return await client.obter_venda_pdv(arguments.get("id"))
    elif tool_name == "tiny_boleto_gerar":
        return await client.gerar_boleto(arguments.get("conta_receber_id"))
    elif tool_name == "tiny_boleto_obter":
        return await client.obter_boleto(arguments.get("id"))
    elif tool_name == "tiny_conta_obter_info":
        return await client.obter_info_conta()

    # RELATÓRIOS
    elif tool_name == "tiny_relatorio_vendas":
        return await client.relatorio_vendas(
            arguments.get("data_inicio"),
            arguments.get("data_fim"),
            arguments.get("tipo", "geral")
        )
    elif tool_name == "tiny_relatorio_produtos_mais_vendidos":
        return await client.relatorio_produtos_mais_vendidos(
            arguments.get("data_inicio"),
            arguments.get("data_fim"),
            arguments.get("limite", 10)
        )
    elif tool_name == "tiny_relatorio_estoque_baixo":
        return await client.relatorio_estoque_baixo(arguments.get("minimo", 5))

    # MOVIMENTAÇÕES
    elif tool_name == "tiny_movimentacoes_estoque_pesquisar":
        return await client.pesquisar_movimentacoes_estoque(**arguments)
    elif tool_name == "tiny_movimentacao_estoque_incluir":
        return await client.incluir_movimentacao_estoque(arguments.get("movimentacao"))

    # CAMPOS PERSONALIZADOS
    elif tool_name == "tiny_campos_personalizados_listar":
        return await client.listar_campos_personalizados(arguments.get("modulo"))

    # WEBHOOKS
    elif tool_name == "tiny_webhooks_listar":
        return await client.listar_webhooks()
    elif tool_name == "tiny_webhook_cadastrar":
        return await client.cadastrar_webhook(arguments.get("url"), arguments.get("eventos"))
    elif tool_name == "tiny_webhook_remover":
        return await client.remover_webhook(arguments.get("id"))

    # INTEGRAÇÕES & LOGS
    elif tool_name == "tiny_integracoes_listar":
        return await client.listar_integracoes()
    elif tool_name == "tiny_logs_api_obter":
        return await client.obter_logs_api(**arguments)

    # MARKETPLACE
    elif tool_name == "tiny_marketplaces_listar":
        return await client.listar_marketplaces()
    elif tool_name == "tiny_marketplace_sincronizar":
        return await client.sincronizar_marketplace(arguments.get("marketplace"))

    else:
        raise ValueError(f"Unknown tool: {tool_name}")


# =============================================================================
# SECURITY
# =============================================================================

def is_origin_allowed(origin: str) -> bool:
    """Valida Origin header para segurança"""
    allowed_patterns = [".railway.app", "localhost", "127.0.0.1", "gptmaker.ai", "claude.ai"]
    return any(pattern in origin for pattern in allowed_patterns)


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/mcp/info")
async def mcp_info():
    """Endpoint de descoberta do servidor MCP"""
    return JSONResponse(content={
        "serverInfo": get_server_info().model_dump(),
        "capabilities": get_server_capabilities().model_dump(exclude_none=True),
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "supportedVersions": SUPPORTED_VERSIONS,
        "transport": "streamable-http",
        "toolsCount": get_tools_count()
    })


@router.get("/mcp/tools")
async def mcp_tools_documentation():
    """
    Lista todas as ferramentas MCP disponíveis com documentação completa

    Este endpoint retorna a lista de todas as 77+ ferramentas do Tiny ERP
    que podem ser chamadas via MCP JSON-RPC no endpoint POST /mcp
    """
    tools = get_all_tools()
    return JSONResponse(content={
        "total": len(tools),
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            }
            for tool in tools
        ]
    })


@router.post("/mcp")
@router.get("/mcp")
async def mcp_endpoint(
    request: Request,
    authorization: Optional[str] = Header(None),
    mcp_protocol_version: Optional[str] = Header(None, alias="MCP-Protocol-Version")
):
    """
    MCP Endpoint - Streamable HTTP Transport
    Suporta GET (SSE stream) e POST (JSON-RPC)
    """

    # Valida origin
    origin = request.headers.get("origin")
    if origin and not is_origin_allowed(origin):
        raise HTTPException(status_code=403, detail="Origin not allowed")

    # Autentica e extrai tiny_token do JWT
    auth_data = await get_auth_data(authorization)
    tenant_id = auth_data["tenant_id"]
    tiny_token = auth_data["tiny_token"]

    # GET: Abre stream SSE
    if request.method == "GET":
        async def keepalive_stream():
            while True:
                yield f"data: {json.dumps({'type': 'keepalive', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                await asyncio.sleep(30)

        return StreamingResponse(
            keepalive_stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
        )

    # POST: Processa JSON-RPC
    try:
        body = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Gerencia sessão
    session_id = body.get("_meta", {}).get("sessionId") or str(uuid.uuid4())

    if session_id not in sessions:
        session = MCPSession(session_id)
        session.tenant_id = tenant_id
        session.tiny_token = tiny_token
        sessions[session_id] = session
    else:
        session = sessions[session_id]

    # Processa requisição
    response_data = await handle_jsonrpc_request(body, session)

    # Notification (sem resposta)
    if response_data is None:
        return Response(status_code=202)

    # Retorna resposta JSON-RPC
    return JSONResponse(
        content=response_data,
        headers={"MCP-Protocol-Version": mcp_protocol_version or MCP_PROTOCOL_VERSION}
    )
