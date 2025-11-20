#!/usr/bin/env node

/**
 * Script de teste para criar pedido no Tiny via MCP
 * Mostra a estrutura CORRETA esperada pela API
 */

const pedidoCorreto = {
  pedido: {
    cliente: {
      // Opção 1: Usar ID do cliente existente
      id: "760308394"

      // Opção 2: Ou informar dados completos para criar novo
      // nome: "Daniel Rudnick",
      // cpf_cnpj: "11283871904",  // sem pontos e traços!
      // email: "d.rudnick.dr@gmail.com"
    },
    itens: [
      {
        item: {  // ← IMPORTANTE: precisa do objeto "item" aninhado!
          id_produto: "953492136",
          descricao: "Teclado Mecânico Gamer, Kalkan Loki, RGB, USB, Switch Marrom, Preto - KLK00013",
          unidade: "PÇ",  // ← IMPORTANTE: precisa da unidade!
          quantidade: "1",  // ← STRING!
          valor_unitario: "154.97"  // ← STRING com ponto decimal!
        }
      }
    ],
    obs: "Pedido via WhatsApp - Iara"
  }
};

console.log("=".repeat(60));
console.log("ESTRUTURA CORRETA PARA CRIAR PEDIDO NO TINY");
console.log("=".repeat(60));
console.log(JSON.stringify(pedidoCorreto, null, 2));
console.log("\n" + "=".repeat(60));
console.log("TESTE CHAMADA MCP");
console.log("=".repeat(60));

const mcpRequest = {
  jsonrpc: "2.0",
  id: 1,
  method: "tools/call",
  params: {
    name: "tiny_pedido_incluir",
    arguments: pedidoCorreto
  }
};

console.log(JSON.stringify(mcpRequest, null, 2));
console.log("\n" + "=".repeat(60));
console.log("DIFERENÇAS IMPORTANTES:");
console.log("=".repeat(60));
console.log("❌ ERRADO: itens: [{ produto_id, quantidade }]");
console.log("✅ CORRETO: itens: [{ item: { id_produto, descricao, unidade, quantidade, valor_unitario } }]");
console.log("");
console.log("❌ ERRADO: contato_id ou nome_cliente");
console.log("✅ CORRETO: cliente: { id: '...' } ou cliente: { nome: '...' }");
console.log("");
console.log("❌ ERRADO: quantidade: 1 (número)");
console.log("✅ CORRETO: quantidade: '1' (string)");
console.log("=".repeat(60));
