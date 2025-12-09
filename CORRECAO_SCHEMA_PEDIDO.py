# CORREÇÃO DO SCHEMA DA TOOL tiny_pedido_incluir
# Substituir no arquivo: src/api/mcp_tools.py (linhas 53-71)

Tool(
    name="tiny_pedido_incluir",
    description="Cria um novo pedido no Tiny ERP",
    inputSchema={
        "type": "object",
        "properties": {
            "pedido": {
                "type": "object",
                "description": "Dados do pedido a ser criado",
                "properties": {
                    "data_pedido": {
                        "type": "string",
                        "description": "Data do pedido no formato DD/MM/YYYY (ex: 28/11/2025)"
                    },
                    "cliente": {
                        "type": "object",
                        "description": "Dados do cliente",
                        "properties": {
                            "nome": {
                                "type": "string",
                                "description": "Nome do cliente (obrigatório)"
                            },
                            "tipo_pessoa": {
                                "type": "string",
                                "description": "F=Física, J=Jurídica",
                                "enum": ["F", "J"]
                            },
                            "cpf_cnpj": {
                                "type": "string",
                                "description": "CPF ou CNPJ do cliente (apenas números)"
                            },
                            "endereco": {
                                "type": "string",
                                "description": "Endereço do cliente"
                            },
                            "numero": {
                                "type": "string",
                                "description": "Número do endereço"
                            },
                            "bairro": {
                                "type": "string",
                                "description": "Bairro"
                            },
                            "cidade": {
                                "type": "string",
                                "description": "Cidade"
                            },
                            "uf": {
                                "type": "string",
                                "description": "Estado (sigla com 2 letras, ex: SP, RJ)"
                            },
                            "cep": {
                                "type": "string",
                                "description": "CEP (apenas números)"
                            },
                            "fone": {
                                "type": "string",
                                "description": "Telefone"
                            },
                            "email": {
                                "type": "string",
                                "description": "Email do cliente"
                            }
                        },
                        "required": ["nome"]
                    },
                    "itens": {
                        "type": "array",
                        "description": "Lista de itens do pedido",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item": {
                                    "type": "object",
                                    "description": "Dados do item",
                                    "properties": {
                                        "codigo": {
                                            "type": "string",
                                            "description": "Código/SKU do produto"
                                        },
                                        "descricao": {
                                            "type": "string",
                                            "description": "Descrição do produto (obrigatório, máx 120 caracteres)"
                                        },
                                        "unidade": {
                                            "type": "string",
                                            "description": "Unidade de medida (obrigatório, ex: UN, PC, KG, CX)"
                                        },
                                        "quantidade": {
                                            "type": "string",
                                            "description": "Quantidade do item (obrigatório)"
                                        },
                                        "valor_unitario": {
                                            "type": "string",
                                            "description": "Valor unitário do produto (obrigatório, formato: 123.45)"
                                        }
                                    },
                                    "required": ["descricao", "unidade", "quantidade", "valor_unitario"]
                                }
                            },
                            "required": ["item"]
                        }
                    },
                    "forma_pagamento": {
                        "type": "string",
                        "description": "Forma de pagamento (ex: boleto, cartao, dinheiro)"
                    },
                    "observacoes": {
                        "type": "string",
                        "description": "Observações do pedido"
                    }
                },
                "required": ["cliente", "itens"]
            }
        },
        "required": ["pedido"]
    }
)


# =============================================================================
# TAMBÉM É NECESSÁRIO CORRIGIR O BUG NO tiny_client.py
# =============================================================================
#
# No arquivo: src/services/tiny_client.py (linha 68-72)
#
# ANTES (com bug - double wrapping):
# async def incluir_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
#     """Inclui novo pedido"""
#     pedido_wrapper = {"pedido": pedido}
#     return await self._request("pedido.incluir", {"pedido": json.dumps(pedido_wrapper)})
#
# DEPOIS (corrigido):
# async def incluir_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
#     """Inclui novo pedido"""
#     return await self._request("pedido.incluir", {"pedido": json.dumps(pedido)})
#
# =============================================================================


# EXEMPLO DE CHAMADA CORRETA APÓS AS CORREÇÕES:
# {
#   "method": "tools/call",
#   "params": {
#     "name": "tiny_pedido_incluir",
#     "arguments": {
#       "pedido": {
#         "data_pedido": "28/11/2025",
#         "cliente": {
#           "nome": "Page Suprimentos de Informatica Ltda",
#           "tipo_pessoa": "J",
#           "cpf_cnpj": "12345678000190",
#           "email": "contato@page.com.br"
#         },
#         "itens": [
#           {
#             "item": {
#               "codigo": "COOLER-V19",
#               "descricao": "Cooler Air Clanm V19, 90mm, Preto",
#               "unidade": "UN",
#               "quantidade": "1",
#               "valor_unitario": "44.97"
#             }
#           }
#         ],
#         "forma_pagamento": "boleto",
#         "observacoes": "Pedido via atendente IA"
#       }
#     }
#   }
# }
