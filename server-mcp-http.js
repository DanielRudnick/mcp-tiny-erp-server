#!/usr/bin/env node

import 'dotenv/config';
import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());

const TINY_TOKEN = process.env.TINY_API_TOKEN;

if (!TINY_TOKEN) {
  console.error("ERRO: TINY_API_TOKEN não configurado!");
  process.exit(1);
}

// ============ TINY API CLIENT ============
class TinyAPI {
  constructor(token) {
    this.token = token;
    this.baseUrl = "https://api.tiny.com.br/api2";
  }

  async request(endpoint, params = {}) {
    const url = new URL(`${this.baseUrl}${endpoint}`);
    url.searchParams.append("token", this.token);
    url.searchParams.append("formato", "json");

    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, value.toString());
      }
    });

    const response = await fetch(url.toString());
    return response.json();
  }

  async requestPost(endpoint, data) {
    const url = new URL(`${this.baseUrl}${endpoint}`);
    url.searchParams.append("token", this.token);
    url.searchParams.append("formato", "json");

    const response = await fetch(url.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams(data)
    });
    return response.json();
  }
}

const tinyAPI = new TinyAPI(TINY_TOKEN);

// ============ MCP TOOLS DEFINITIONS ============
const MCP_TOOLS = [
  {
    name: "tiny_produtos_pesquisar",
    description: "[ESSENCIAL PARA VENDAS] Use esta ferramenta para pesquisar produtos, itens, mercadorias ou qualquer coisa do catálogo quando o cliente quiser saber o preço, estoque ou disponibilidade.",
    inputSchema: {
      type: "object",
      properties: {
        pesquisa: {
          type: "string",
          description: "Nome, código ou SKU do produto",
        },
        pagina: { type: "number", description: "Número da página (padrão: 1)" },
        situacao: {
          type: "string",
          enum: ["A", "I", "E"],
          description: "A=Ativo, I=Inativo, E=Excluído (padrão: A)",
        },
      },
      required: ["pesquisa"],
    },
  },
  {
    name: "tiny_produto_obter",
    description: "Obtém detalhes completos de um produto",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "ID do produto" },
      },
      required: ["id"],
    },
  },
  {
    name: "tiny_pedidos_pesquisar",
    description: "Pesquisa pedidos no Tiny ERP por número, cliente, CPF/CNPJ ou período",
    inputSchema: {
      type: "object",
      properties: {
        pesquisa: {
          type: "string",
          description: "Termo de pesquisa (número, cliente, etc.)",
        },
        pagina: { type: "number", description: "Número da página (padrão: 1)" },
      },
      required: ["pesquisa"],
    },
  },
  {
    name: "tiny_pedido_obter",
    description: "Obtém detalhes completos de um pedido específico",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "ID do pedido" },
      },
      required: ["id"],
    },
  },
  {
    name: "tiny_pedido_incluir",
    description: "Cria um novo pedido no Tiny ERP. IMPORTANTE: Sempre pesquise o produto antes para obter id_produto, descricao, unidade e valor_unitario corretos.",
    inputSchema: {
      type: "object",
      properties: {
        pedido: {
          type: "object",
          description: "Objeto contendo os dados completos do pedido",
          properties: {
            cliente: {
              type: "object",
              description: "Dados do cliente. Use 'id' para cliente existente ou preencha outros campos para criar novo",
              properties: {
                id: { type: "string", description: "ID do cliente no Tiny (se já existir)" },
                nome: { type: "string", description: "Nome completo do cliente" },
                cpf_cnpj: { type: "string", description: "CPF ou CNPJ (apenas números)" },
                email: { type: "string", description: "Email do cliente" },
                fone: { type: "string", description: "Telefone" },
                endereco: { type: "string", description: "Endereço" },
                numero: { type: "string", description: "Número" },
                bairro: { type: "string", description: "Bairro" },
                cidade: { type: "string", description: "Cidade" },
                uf: { type: "string", description: "Estado (UF)" },
                cep: { type: "string", description: "CEP" },
              },
            },
            itens: {
              type: "array",
              description: "Lista de itens do pedido",
              items: {
                type: "object",
                properties: {
                  item: {
                    type: "object",
                    description: "Dados do item",
                    properties: {
                      id_produto: { type: "string", description: "ID do produto no Tiny (obrigatório)" },
                      descricao: { type: "string", description: "Descrição do produto (obrigatório)" },
                      unidade: { type: "string", description: "Unidade de medida (ex: UN, PC, KG)" },
                      quantidade: { type: "string", description: "Quantidade (formato: '1', '2.5')" },
                      valor_unitario: { type: "string", description: "Valor unitário (formato: '100.00')" },
                    },
                    required: ["id_produto", "descricao", "unidade", "quantidade", "valor_unitario"],
                  },
                },
                required: ["item"],
              },
            },
            data_pedido: { type: "string", description: "Data do pedido (DD/MM/YYYY)" },
            obs: { type: "string", description: "Observações do pedido" },
            forma_pagamento: { type: "string", description: "Forma de pagamento (ex: dinheiro, boleto, pix)" },
          },
          required: ["cliente", "itens"],
        },
      },
      required: ["pedido"],
    },
  },
  {
    name: "tiny_contatos_pesquisar",
    description: "Pesquisa contatos/clientes",
    inputSchema: {
      type: "object",
      properties: {
        pesquisa: { type: "string", description: "Nome, CPF, CNPJ" },
        pagina: { type: "number", description: "Número da página (padrão: 1)" },
      },
      required: ["pesquisa"],
    },
  },
  {
    name: "tiny_contato_obter",
    description: "Obtém detalhes de um contato",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "ID do contato" },
      },
      required: ["id"],
    },
  },
  {
    name: "tiny_contato_incluir",
    description: "Cadastra novo contato/cliente",
    inputSchema: {
      type: "object",
      properties: {
        contato: {
          type: "object",
          description: "Dados do contato (nome, cpf_cnpj, email, etc.)",
        },
      },
      required: ["contato"],
    },
  },
];

// ============ MCP HANDLERS ============
async function handleToolCall(toolName, args) {
  try {
    switch (toolName) {
      case "tiny_produtos_pesquisar": {
        const result = await tinyAPI.request("/produtos.pesquisa.php", args);
        return { success: true, data: result };
      }

      case "tiny_produto_obter": {
        const result = await tinyAPI.request("/produto.obter.php", args);
        return { success: true, data: result };
      }

      case "tiny_pedidos_pesquisar": {
        const result = await tinyAPI.request("/pedidos.pesquisa.php", args);
        return { success: true, data: result };
      }

      case "tiny_pedido_obter": {
        const result = await tinyAPI.request("/pedido.obter.php", args);
        return { success: true, data: result };
      }

      case "tiny_pedido_incluir": {
        const result = await tinyAPI.requestPost("/pedido.incluir.php", {
          pedido: JSON.stringify(args.pedido)
        });
        return { success: true, data: result };
      }

      case "tiny_contatos_pesquisar": {
        const result = await tinyAPI.request("/contatos.pesquisa.php", args);
        return { success: true, data: result };
      }

      case "tiny_contato_obter": {
        const result = await tinyAPI.request("/contato.obter.php", args);
        return { success: true, data: result };
      }

      case "tiny_contato_incluir": {
        const result = await tinyAPI.requestPost("/contato.incluir.php", {
          contato: JSON.stringify({ contato: args.contato })
        });
        return { success: true, data: result };
      }

      default:
        throw new Error(`Ferramenta desconhecida: ${toolName}`);
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

// ============ MCP ENDPOINTS ============

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "tiny-mcp-server",
    version: "2.0.0",
    protocol: "MCP over HTTP",
    tools: MCP_TOOLS.length,
  });
});

// MCP: Initialize (stateless)
app.post("/mcp/initialize", (req, res) => {
  res.json({
    jsonrpc: "2.0",
    id: req.body.id || 1,
    result: {
      protocolVersion: "2025-06-18",
      capabilities: {
        tools: {},
      },
      serverInfo: {
        name: "tiny-erp-server",
        version: "2.0.0",
      },
    },
  });
});

// MCP: List tools
app.post("/mcp/tools/list", (req, res) => {
  res.json({
    jsonrpc: "2.0",
    id: req.body.id || 1,
    result: {
      tools: MCP_TOOLS,
    },
  });
});

// MCP: Call tool
app.post("/mcp/tools/call", async (req, res) => {
  const { id, params } = req.body;
  const { name, arguments: args } = params || {};

  if (!name) {
    return res.json({
      jsonrpc: "2.0",
      id: id || 1,
      error: {
        code: -32602,
        message: "Invalid params: 'name' is required",
      },
    });
  }

  try {
    const result = await handleToolCall(name, args || {});

    res.json({
      jsonrpc: "2.0",
      id: id || 1,
      result: {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      },
    });
  } catch (error) {
    res.json({
      jsonrpc: "2.0",
      id: id || 1,
      error: {
        code: -32603,
        message: error.message,
      },
    });
  }
});

// Generic MCP endpoint (handles all methods)
app.post("/mcp", async (req, res) => {
  const { jsonrpc, id, method, params } = req.body;

  if (jsonrpc !== "2.0") {
    return res.json({
      jsonrpc: "2.0",
      id: id || 1,
      error: {
        code: -32600,
        message: "Invalid Request: jsonrpc must be '2.0'",
      },
    });
  }

  try {
    switch (method) {
      case "initialize":
        res.json({
          jsonrpc: "2.0",
          id,
          result: {
            protocolVersion: "2025-06-18",
            capabilities: { tools: {} },
            serverInfo: {
              name: "tiny-erp-server",
              version: "2.0.0",
            },
          },
        });
        break;

      case "notifications/initialized":
        res.status(204).send();
        break;

      case "tools/list":
        res.json({
          jsonrpc: "2.0",
          id,
          result: { tools: MCP_TOOLS },
        });
        break;

      case "tools/call": {
        const { name, arguments: args } = params || {};
        const result = await handleToolCall(name, args || {});

        res.json({
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          },
        });
        break;
      }

      default:
        res.json({
          jsonrpc: "2.0",
          id,
          error: {
            code: -32601,
            message: `Method not found: ${method}`,
          },
        });
    }
  } catch (error) {
    res.json({
      jsonrpc: "2.0",
      id,
      error: {
        code: -32603,
        message: error.message,
      },
    });
  }
});

// CORS
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`\n🚀 Servidor MCP HTTP v2.0 rodando!`);
  console.log(`📡 Porta: ${PORT}`);
  console.log(`🔗 Health: http://localhost:${PORT}/health`);
  console.log(`🔧 MCP: http://localhost:${PORT}/mcp`);
  console.log(`\n📋 Endpoints MCP disponíveis:`);
  console.log(`   POST /mcp/initialize`);
  console.log(`   POST /mcp/tools/list`);
  console.log(`   POST /mcp/tools/call`);
  console.log(`   POST /mcp (generic endpoint)`);
  console.log(`\n✨ ${MCP_TOOLS.length} ferramentas carregadas!`);
  console.log(`✨ Pronto para integrar com Sellflux, n8n, Make, etc!\n`);
});
