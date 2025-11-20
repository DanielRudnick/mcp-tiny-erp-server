#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fetch from "node-fetch";

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

    try {
      const response = await fetch(url.toString());
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error(`Erro na requisição ao Tiny: ${error.message}`);
    }
  }

  async pesquisarProdutos(pesquisa, pagina = 1, situacao = "A") {
    return this.request("/produtos.pesquisa.php", {
      pesquisa,
      pagina,
      situacao,
    });
  }

  async obterProduto(id) {
    return this.request("/produto.obter.php", { id });
  }

  async pesquisarPedidos(pesquisa, pagina = 1) {
    return this.request("/pedidos.pesquisa.php", {
      pesquisa,
      pagina,
    });
  }

  async obterPedido(id) {
    return this.request("/pedido.obter.php", { id });
  }
}

const server = new Server(
  {
    name: "tiny-erp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

const TINY_TOKEN = process.env.TINY_API_TOKEN;

if (!TINY_TOKEN) {
  console.error("ERRO: TINY_API_TOKEN não configurado!");
  console.error("Configure a variável de ambiente TINY_API_TOKEN com seu token da API do Tiny");
  process.exit(1);
}

const tinyAPI = new TinyAPI(TINY_TOKEN);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "tiny_produtos_pesquisar",
        description: "Pesquisa produtos no Tiny (ex.: nome, código, gtin).",
        inputSchema: {
          type: "object",
          properties: {
            pesquisa: {
              type: "string",
              description: "Termo de busca (nome, código, GTIN do produto)",
            },
            pagina: {
              type: "number",
              description: "Número da página (padrão: 1)",
            },
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
        description: "Obtém detalhes de um produto pelo 'id'.",
        inputSchema: {
          type: "object",
          properties: {
            id: {
              type: "string",
              description: "ID do produto no Tiny",
            },
          },
          required: ["id"],
        },
      },
      {
        name: "tiny_pedidos_pesquisar",
        description: "Pesquisa pedidos no Tiny (ex.: número, cliente:nome).",
        inputSchema: {
          type: "object",
          properties: {
            pesquisa: {
              type: "string",
              description: "Termo de busca (número do pedido, nome do cliente, etc.)",
            },
            pagina: {
              type: "number",
              description: "Número da página (padrão: 1)",
            },
          },
          required: ["pesquisa"],
        },
      },
      {
        name: "tiny_pedido_obter",
        description: "Obtém detalhes de um pedido pelo 'id' (não confundir com número).",
        inputSchema: {
          type: "object",
          properties: {
            id: {
              type: "string",
              description: "ID do pedido no Tiny",
            },
          },
          required: ["id"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "tiny_produtos_pesquisar": {
        const result = await tinyAPI.pesquisarProdutos(
          args.pesquisa,
          args.pagina,
          args.situacao
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "tiny_produto_obter": {
        const result = await tinyAPI.obterProduto(args.id);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "tiny_pedidos_pesquisar": {
        const result = await tinyAPI.pesquisarPedidos(
          args.pesquisa,
          args.pagina
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case "tiny_pedido_obter": {
        const result = await tinyAPI.obterPedido(args.id);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Ferramenta desconhecida: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Erro: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Servidor MCP do Tiny iniciado com sucesso!");
}

main().catch((error) => {
  console.error("Erro ao iniciar servidor:", error);
  process.exit(1);
});
