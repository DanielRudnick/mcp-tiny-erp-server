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

  // PRODUTOS
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

  // CLIENTES (CONTATOS)
  async pesquisarContatos(pesquisa, pagina = 1) {
    return this.request("/contatos.pesquisa.php", {
      pesquisa,
      pagina,
    });
  }

  async obterContato(id) {
    return this.request("/contato.obter.php", { id });
  }

  async incluirContato(dadosCliente) {
    return this.requestPost("/contato.incluir.php", {
      contato: JSON.stringify({ contato: dadosCliente })
    });
  }

  // PEDIDOS
  async pesquisarPedidos(pesquisa, pagina = 1) {
    return this.request("/pedidos.pesquisa.php", {
      pesquisa,
      pagina,
    });
  }

  async obterPedido(id) {
    return this.request("/pedido.obter.php", { id });
  }

  async incluirPedido(dadosPedido) {
    return this.requestPost("/pedido.incluir.php", {
      pedido: JSON.stringify({ pedido: dadosPedido })
    });
  }

  // NOTA FISCAL
  async incluirNotaFiscal(dadosNota) {
    return this.requestPost("/nota.fiscal.incluir.php", {
      nota: JSON.stringify({ nota_fiscal: dadosNota })
    });
  }

  async emitirNotaFiscal(id) {
    return this.requestPost("/nota.fiscal.emitir.php", {
      id: id
    });
  }

  async obterNotaFiscal(id) {
    return this.request("/nota.fiscal.obter.php", { id });
  }

  async obterLinkNotaFiscal(id) {
    return this.request("/nota.fiscal.obter.link.php", { id });
  }
}

const tinyAPI = new TinyAPI(TINY_TOKEN);

// HEALTH CHECK
app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "tiny-api-server", version: "2.0" });
});

// ============ PRODUTOS ============
app.post("/produtos/pesquisar", async (req, res) => {
  try {
    const { pesquisa, pagina, situacao } = req.body;
    if (!pesquisa) {
      return res.status(400).json({ error: "Parâmetro 'pesquisa' é obrigatório" });
    }
    const result = await tinyAPI.pesquisarProdutos(pesquisa, pagina, situacao);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/produtos/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const result = await tinyAPI.obterProduto(id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ CLIENTES (CONTATOS) ============
app.post("/contatos/pesquisar", async (req, res) => {
  try {
    const { pesquisa, pagina } = req.body;
    if (!pesquisa) {
      return res.status(400).json({ error: "Parâmetro 'pesquisa' é obrigatório" });
    }
    const result = await tinyAPI.pesquisarContatos(pesquisa, pagina);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/contatos/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const result = await tinyAPI.obterContato(id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post("/contatos/incluir", async (req, res) => {
  try {
    const dadosCliente = req.body;
    if (!dadosCliente.nome) {
      return res.status(400).json({ error: "Campo 'nome' é obrigatório" });
    }
    const result = await tinyAPI.incluirContato(dadosCliente);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ PEDIDOS ============
app.post("/pedidos/pesquisar", async (req, res) => {
  try {
    const { pesquisa, pagina } = req.body;
    if (!pesquisa) {
      return res.status(400).json({ error: "Parâmetro 'pesquisa' é obrigatório" });
    }
    const result = await tinyAPI.pesquisarPedidos(pesquisa, pagina);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/pedidos/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const result = await tinyAPI.obterPedido(id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post("/pedidos/incluir", async (req, res) => {
  try {
    const dadosPedido = req.body;
    if (!dadosPedido.cliente || !dadosPedido.itens) {
      return res.status(400).json({
        error: "Campos 'cliente' e 'itens' são obrigatórios"
      });
    }
    const result = await tinyAPI.incluirPedido(dadosPedido);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ NOTA FISCAL ============
app.post("/notafiscal/incluir", async (req, res) => {
  try {
    const dadosNota = req.body;
    const result = await tinyAPI.incluirNotaFiscal(dadosNota);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post("/notafiscal/emitir", async (req, res) => {
  try {
    const { id } = req.body;
    if (!id) {
      return res.status(400).json({ error: "Campo 'id' é obrigatório" });
    }
    const result = await tinyAPI.emitirNotaFiscal(id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/notafiscal/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const result = await tinyAPI.obterNotaFiscal(id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/notafiscal/:id/link", async (req, res) => {
  try {
    const { id } = req.params;
    const result = await tinyAPI.obterLinkNotaFiscal(id);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============ ENDPOINT COMPLETO PARA SELLFLUX ============
app.post("/venda/completa", async (req, res) => {
  try {
    const { cpf_cnpj, cliente, produto_id, quantidade, forma_pagamento } = req.body;

    // 1. Buscar cliente
    let clienteId;
    const buscaCliente = await tinyAPI.pesquisarContatos(cpf_cnpj);

    if (buscaCliente.retorno.contatos && buscaCliente.retorno.contatos.length > 0) {
      clienteId = buscaCliente.retorno.contatos[0].contato.id;
    } else {
      // 2. Criar cliente se não existir
      const novoCliente = await tinyAPI.incluirContato(cliente);
      clienteId = novoCliente.retorno.registros[0].registro.id;
    }

    // 3. Buscar produto
    const produto = await tinyAPI.obterProduto(produto_id);
    const dadosProduto = produto.retorno.produto;

    // 4. Criar pedido
    const pedido = {
      cliente: { id: clienteId },
      itens: [{
        item: {
          codigo: dadosProduto.codigo,
          descricao: dadosProduto.nome,
          unidade: "UN",
          quantidade: quantidade.toString(),
          valor_unitario: dadosProduto.preco
        }
      }],
      parcelas: [{
        parcela: {
          dias: "0",
          valor: (parseFloat(dadosProduto.preco) * quantidade).toFixed(2),
          forma_pagamento: forma_pagamento
        }
      }]
    };

    const novoPedido = await tinyAPI.incluirPedido(pedido);
    const pedidoId = novoPedido.retorno.registros[0].registro.id;

    // 5. Gerar nota fiscal
    const nota = {
      id_pedido: pedidoId,
      tipo: "S",
      natureza_operacao: "Venda",
      modelo: "55"
    };

    const notaFiscal = await tinyAPI.incluirNotaFiscal(nota);
    const notaId = notaFiscal.retorno.registros[0].registro.id;

    // 6. Emitir nota fiscal
    await tinyAPI.emitirNotaFiscal(notaId);

    // 7. Obter link da nota
    const linkNota = await tinyAPI.obterLinkNotaFiscal(notaId);

    res.json({
      sucesso: true,
      pedido_id: pedidoId,
      nota_fiscal_id: notaId,
      link_nota: linkNota.retorno.link,
      mensagem: "Venda realizada com sucesso!"
    });

  } catch (error) {
    res.status(500).json({
      sucesso: false,
      error: error.message
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`\n🚀 Servidor Tiny API v2.0 rodando!`);
  console.log(`📡 Porta: ${PORT}`);
  console.log(`🔗 Health: http://localhost:${PORT}/health`);
  console.log(`\n📋 Endpoints disponíveis:`);
  console.log(`   Produtos: /produtos/*`);
  console.log(`   Clientes: /contatos/*`);
  console.log(`   Pedidos: /pedidos/*`);
  console.log(`   NF-e: /notafiscal/*`);
  console.log(`   Venda Completa: POST /venda/completa`);
  console.log(`\n✨ Pronto para integrar com Sellflux!\n`);
});
