#!/usr/bin/env node

import fetch from "node-fetch";

console.log("🧪 Testando configuração do Servidor Tiny MCP\n");
console.log("=".repeat(50));

console.log("\n1️⃣ Verificando token da API...");
const token = process.env.TINY_API_TOKEN;

if (!token) {
  console.error("❌ ERRO: TINY_API_TOKEN não configurado!");
  console.error("Configure a variável de ambiente ou o arquivo .env");
  process.exit(1);
}

console.log("✅ Token encontrado:", token.substring(0, 10) + "...");

console.log("\n2️⃣ Testando conexão com API do Tiny...");

const testUrl = `https://api.tiny.com.br/api2/info.php?token=${token}&formato=json`;

try {
  const response = await fetch(testUrl);
  const data = await response.json();
  
  if (data.retorno && data.retorno.status_processamento === "3") {
    console.log("✅ Conexão com Tiny OK!");
    console.log("   Conta:", data.retorno.conta || "N/A");
  } else if (data.retorno && data.retorno.status_processamento === "2") {
    console.error("❌ ERRO: Token inválido!");
    console.error("Verifique seu token no Tiny ERP");
    process.exit(1);
  } else {
    console.log("⚠️  Resposta inesperada da API:");
    console.log(JSON.stringify(data, null, 2));
  }
} catch (error) {
  console.error("❌ ERRO ao conectar com Tiny:", error.message);
  console.error("Verifique sua conexão com internet");
  process.exit(1);
}

console.log("\n3️⃣ Verificando dependências...");

try {
  const { Server } = await import("@modelcontextprotocol/sdk/server/index.js");
  console.log("✅ SDK MCP instalado");
} catch (error) {
  console.error("❌ SDK MCP não encontrado!");
  console.error("Execute: npm install");
  process.exit(1);
}

try {
  const express = await import("express");
  console.log("✅ Express instalado");
} catch (error) {
  console.error("❌ Express não encontrado!");
  console.error("Execute: npm install");
  process.exit(1);
}

console.log("\n" + "=".repeat(50));
console.log("🎉 Tudo configurado corretamente!");
console.log("\nPróximos passos:");
console.log("  • Para Claude Desktop: npm start");
console.log("  • Para N8N: npm run start:http");
console.log("\n" + "=".repeat(50));
