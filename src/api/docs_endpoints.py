"""
Endpoints de documentação visual
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from src.api.mcp_tools import TOOLS

router = APIRouter(prefix="/docs-mcp", tags=["📚 Documentação MCP"])


@router.get("/", response_class=HTMLResponse, summary="Documentação visual das tools MCP")
async def docs_html():
    """
    Página HTML com documentação visual de todas as 77 tools MCP organizadas por categoria
    """

    # Organizar tools por categoria
    categorias = {
        "Pedidos": [],
        "Produtos": [],
        "Contatos": [],
        "Notas Fiscais": [],
        "Financeiro": [],
        "CRM": [],
        "Outros": []
    }

    for tool in TOOLS:
        if "pedido" in tool.name:
            categorias["Pedidos"].append(tool)
        elif "produto" in tool.name:
            categorias["Produtos"].append(tool)
        elif "contato" in tool.name:
            categorias["Contatos"].append(tool)
        elif "nota" in tool.name or "nf" in tool.name:
            categorias["Notas Fiscais"].append(tool)
        elif "conta" in tool.name or "boleto" in tool.name:
            categorias["Financeiro"].append(tool)
        elif "crm" in tool.name or "oportunidade" in tool.name:
            categorias["CRM"].append(tool)
        else:
            categorias["Outros"].append(tool)

    # Gerar HTML
    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Tiny ERP - Documentação das Tools</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 1.2em;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }
        .stat {
            background: #f8f9fa;
            padding: 15px 25px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .category {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        .category-title {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        .tool {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #764ba2;
            transition: all 0.3s ease;
        }
        .tool:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .tool-name {
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
            font-weight: bold;
            color: #764ba2;
            margin-bottom: 10px;
        }
        .tool-description {
            color: #555;
            margin-bottom: 15px;
        }
        .schema-toggle {
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s;
        }
        .schema-toggle:hover {
            background: #5568d3;
        }
        .schema {
            display: none;
            background: #2d3748;
            color: #68d391;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .schema.show {
            display: block;
        }
        footer {
            text-align: center;
            color: white;
            padding: 30px;
            margin-top: 40px;
        }
        .badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 MCP Tiny ERP Server</h1>
            <p class="subtitle">Documentação completa das Tools - Model Context Protocol</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">""" + str(len(TOOLS)) + """</div>
                    <div class="stat-label">Tools Disponíveis</div>
                </div>
                <div class="stat">
                    <div class="stat-number">""" + str(len([c for c in categorias.values() if c])) + """</div>
                    <div class="stat-label">Categorias</div>
                </div>
                <div class="stat">
                    <div class="stat-number">v2.0</div>
                    <div class="stat-label">Versão</div>
                </div>
            </div>
        </header>
"""

    # Adicionar cada categoria
    for categoria, tools in categorias.items():
        if not tools:
            continue

        html += f"""
        <div class="category">
            <h2 class="category-title">{categoria} <span class="badge">{len(tools)} tools</span></h2>
"""

        for tool in tools:
            import json
            schema_json = json.dumps(tool.inputSchema, indent=2, ensure_ascii=False)

            html += f"""
            <div class="tool">
                <div class="tool-name">{tool.name}</div>
                <div class="tool-description">{tool.description}</div>
                <button class="schema-toggle" onclick="toggleSchema('{tool.name}')">
                    Ver Schema JSON
                </button>
                <div class="schema" id="schema-{tool.name}">
                    <pre>{schema_json}</pre>
                </div>
            </div>
"""

        html += """
        </div>
"""

    html += """
        <footer>
            <p>MCP Tiny ERP Server | Integração completa com Tiny ERP via Model Context Protocol</p>
            <p style="margin-top: 10px; opacity: 0.8;">
                <a href="/docs" style="color: white;">Swagger Docs</a> |
                <a href="/tools" style="color: white;">API JSON</a> |
                <a href="/health" style="color: white;">Health Check</a>
            </p>
        </footer>
    </div>

    <script>
        function toggleSchema(toolName) {
            const schema = document.getElementById('schema-' + toolName);
            schema.classList.toggle('show');
        }
    </script>
</body>
</html>
"""

    return HTMLResponse(content=html)


@router.get("/json", summary="Lista todas as tools em formato JSON")
async def docs_json():
    """
    Retorna todas as tools organizadas por categoria em formato JSON
    """
    categorias = {
        "pedidos": [],
        "produtos": [],
        "contatos": [],
        "notas_fiscais": [],
        "financeiro": [],
        "crm": [],
        "outros": []
    }

    for tool in TOOLS:
        tool_data = {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.inputSchema
        }

        if "pedido" in tool.name:
            categorias["pedidos"].append(tool_data)
        elif "produto" in tool.name:
            categorias["produtos"].append(tool_data)
        elif "contato" in tool.name:
            categorias["contatos"].append(tool_data)
        elif "nota" in tool.name or "nf" in tool.name:
            categorias["notas_fiscais"].append(tool_data)
        elif "conta" in tool.name or "boleto" in tool.name:
            categorias["financeiro"].append(tool_data)
        elif "crm" in tool.name or "oportunidade" in tool.name:
            categorias["crm"].append(tool_data)
        else:
            categorias["outros"].append(tool_data)

    return JSONResponse(content={
        "total_tools": len(TOOLS),
        "categorias": categorias
    })
