"""
Catálogo completo de ferramentas MCP para API Tiny ERP
Mapeia ~120 endpoints para ferramentas utilizáveis via MCP Protocol
"""

from typing import List, Dict, Any
from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]


# =============================================================================
# CATÁLOGO COMPLETO DE FERRAMENTAS (~120 ferramentas)
# =============================================================================

TOOLS_CATALOG: List[Tool] = [
    
    # =========================================================================
    # PEDIDOS / VENDAS (7 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_pedidos_pesquisar",
        description="Pesquisa pedidos no Tiny ERP por número, cliente, CPF/CNPJ ou período",
        inputSchema={
            "type": "object",
            "properties": {
                "pesquisa": {"type": "string", "description": "Termo de pesquisa"},
                "pagina": {"type": "integer", "default": 1, "minimum": 1},
                "data_inicio": {"type": "string", "description": "Data início (DD/MM/YYYY)"},
                "data_fim": {"type": "string", "description": "Data fim (DD/MM/YYYY)"}
            },
            "required": ["pesquisa"]
        }
    ),
    
    Tool(
        name="tiny_pedido_obter",
        description="Obtém detalhes completos de um pedido específico",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do pedido"}
            },
            "required": ["id"]
        }
    ),
    
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
                            "description": "Data do pedido no formato DD/MM/YYYY"
                        },
                        "cliente": {
                            "type": "object",
                            "description": "Dados do cliente",
                            "properties": {
                                "nome": {"type": "string", "description": "Nome do cliente (obrigatorio)"},
                                "tipo_pessoa": {"type": "string", "description": "F=Fisica, J=Juridica", "enum": ["F", "J"]},
                                "cpf_cnpj": {"type": "string", "description": "CPF ou CNPJ do cliente"},
                                "endereco": {"type": "string", "description": "Endereco do cliente"},
                                "numero": {"type": "string", "description": "Numero do endereco"},
                                "bairro": {"type": "string", "description": "Bairro"},
                                "cidade": {"type": "string", "description": "Cidade"},
                                "uf": {"type": "string", "description": "Estado (UF)"},
                                "cep": {"type": "string", "description": "CEP"},
                                "fone": {"type": "string", "description": "Telefone"},
                                "email": {"type": "string", "description": "Email do cliente"}
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
                                            "codigo": {"type": "string", "description": "Codigo/SKU do produto"},
                                            "descricao": {"type": "string", "description": "Descricao do produto (obrigatorio)"},
                                            "unidade": {"type": "string", "description": "Unidade de medida (obrigatorio, ex: UN, PC, KG)"},
                                            "quantidade": {"type": "string", "description": "Quantidade do item (obrigatorio)"},
                                            "valor_unitario": {"type": "string", "description": "Valor unitario (obrigatorio)"}
                                        },
                                        "required": ["descricao", "unidade", "quantidade", "valor_unitario"]
                                    }
                                },
                                "required": ["item"]
                            }
                        },
                        "forma_pagamento": {"type": "string", "description": "Forma de pagamento"},
                        "observacoes": {"type": "string", "description": "Observacoes do pedido"}
                    },
                    "required": ["cliente", "itens"]
                }
            },
            "required": ["pedido"]
        }
    ),
    
    Tool(
        name="tiny_pedido_alterar",
        description="Altera um pedido existente",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do pedido"},
                "pedido": {"type": "object", "description": "Dados atualizados"}
            },
            "required": ["id", "pedido"]
        }
    ),
    
    Tool(
        name="tiny_pedido_alterar_situacao",
        description="Altera a situação de um pedido",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do pedido"},
                "situacao": {"type": "string", "description": "Nova situação"}
            },
            "required": ["id", "situacao"]
        }
    ),
    
    Tool(
        name="tiny_pedido_obter_rastreamento",
        description="Obtém informações de rastreamento de um pedido",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do pedido"}
            },
            "required": ["id"]
        }
    ),
    
    # =========================================================================
    # PRODUTOS (7 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_produtos_pesquisar",
        description="Pesquisa produtos no Tiny ERP. IMPORTANTE: A pesquisa do Tiny é EXATA - precisa usar o nome COMPLETO do produto como está cadastrado no sistema. Use a ferramenta products_269836_list PRIMEIRO para encontrar produtos (ela tem busca inteligente), depois use esta ferramenta com o NOME EXATO retornado para obter preço e estoque atualizados do Tiny.",
        inputSchema={
            "type": "object",
            "properties": {
                "pesquisa": {"type": "string", "description": "Nome COMPLETO e EXATO do produto como cadastrado no Tiny (ex: 'Processador Intel Core i5-9500' ao invés de 'i5 9ª geração')"},
                "pagina": {"type": "integer", "default": 1},
                "situacao": {"type": "string", "enum": ["A", "I", "E"], "default": "A", "description": "A=Ativo, I=Inativo, E=Excluído"},
                "gtin": {"type": "string", "description": "Código de barras (EAN)"}
            },
            "required": ["pesquisa"]
        }
    ),
    
    Tool(
        name="tiny_produto_obter",
        description="Obtém TODOS os dados atualizados de um produto (preço em tempo real, estoque atual, descrição completa, categoria, marca, imagens, etc). Use esta ferramenta após buscar produtos para obter informações precisas e atualizadas do sistema Tiny.",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do produto retornado pela busca"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_produto_incluir",
        description="Cadastra um novo produto",
        inputSchema={
            "type": "object",
            "properties": {
                "produto": {"type": "object", "description": "Dados do produto"}
            },
            "required": ["produto"]
        }
    ),
    
    Tool(
        name="tiny_produto_alterar",
        description="Altera um produto existente",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do produto"},
                "produto": {"type": "object", "description": "Dados atualizados"}
            },
            "required": ["id", "produto"]
        }
    ),
    
    Tool(
        name="tiny_produto_obter_estoque",
        description="Obtém estoque atual de um produto",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do produto"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_produto_atualizar_estoque",
        description="Atualiza estoque de um produto",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do produto"},
                "estoque": {"type": "number", "description": "Quantidade"}
            },
            "required": ["id", "estoque"]
        }
    ),
    
    Tool(
        name="tiny_produto_obter_preco",
        description="Obtém preço de um produto",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do produto"}
            },
            "required": ["id"]
        }
    ),
    
    # =========================================================================
    # CONTATOS / CLIENTES (4 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_contatos_pesquisar",
        description="Pesquisa contatos/clientes",
        inputSchema={
            "type": "object",
            "properties": {
                "pesquisa": {"type": "string", "description": "Nome, CPF, CNPJ"},
                "pagina": {"type": "integer", "default": 1},
                "tipo_pessoa": {"type": "string", "enum": ["F", "J"]}
            },
            "required": ["pesquisa"]
        }
    ),
    
    Tool(
        name="tiny_contato_obter",
        description="Obtém detalhes de um contato",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do contato"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_contato_incluir",
        description="Cadastra novo contato/cliente no Tiny ERP",
        inputSchema={
            "type": "object",
            "properties": {
                "contato": {
                    "type": "object",
                    "description": "Dados do contato/cliente",
                    "properties": {
                        "nome": {"type": "string", "description": "Nome completo (obrigatorio)"},
                        "tipo_pessoa": {"type": "string", "description": "F=Fisica, J=Juridica", "enum": ["F", "J"]},
                        "cpf_cnpj": {"type": "string", "description": "CPF (11 digitos) ou CNPJ (14 digitos)"},
                        "endereco": {"type": "string", "description": "Endereco completo"},
                        "numero": {"type": "string", "description": "Numero do endereco"},
                        "complemento": {"type": "string", "description": "Complemento"},
                        "bairro": {"type": "string", "description": "Bairro"},
                        "cidade": {"type": "string", "description": "Cidade"},
                        "uf": {"type": "string", "description": "Estado (UF - 2 letras)"},
                        "cep": {"type": "string", "description": "CEP"},
                        "fone": {"type": "string", "description": "Telefone fixo"},
                        "celular": {"type": "string", "description": "Celular"},
                        "email": {"type": "string", "description": "Email"}
                    },
                    "required": ["nome"]
                }
            },
            "required": ["contato"]
        }
    ),
    
    Tool(
        name="tiny_contato_alterar",
        description="Altera contato/cliente existente no Tiny ERP",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do contato no Tiny ERP"},
                "contato": {
                    "type": "object",
                    "description": "Dados a serem atualizados",
                    "properties": {
                        "nome": {"type": "string", "description": "Nome completo"},
                        "tipo_pessoa": {"type": "string", "description": "F=Fisica, J=Juridica", "enum": ["F", "J"]},
                        "cpf_cnpj": {"type": "string", "description": "CPF ou CNPJ"},
                        "endereco": {"type": "string", "description": "Endereco"},
                        "numero": {"type": "string", "description": "Numero"},
                        "complemento": {"type": "string", "description": "Complemento"},
                        "bairro": {"type": "string", "description": "Bairro"},
                        "cidade": {"type": "string", "description": "Cidade"},
                        "uf": {"type": "string", "description": "UF"},
                        "cep": {"type": "string", "description": "CEP"},
                        "fone": {"type": "string", "description": "Telefone"},
                        "celular": {"type": "string", "description": "Celular"},
                        "email": {"type": "string", "description": "Email"}
                    }
                }
            },
            "required": ["id", "contato"]
        }
    ),
    
    # =========================================================================
    # NOTAS FISCAIS (7 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_notas_fiscais_pesquisar",
        description="Pesquisa notas fiscais",
        inputSchema={
            "type": "object",
            "properties": {
                "pesquisa": {"type": "string"},
                "pagina": {"type": "integer", "default": 1},
                "data_inicio": {"type": "string"},
                "data_fim": {"type": "string"}
            },
            "required": ["pesquisa"]
        }
    ),
    
    Tool(
        name="tiny_nota_fiscal_obter",
        description="Obtém detalhes de uma nota fiscal",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da nota fiscal"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_nota_fiscal_incluir",
        description="Emite nova nota fiscal",
        inputSchema={
            "type": "object",
            "properties": {
                "nota": {"type": "object", "description": "Dados da nota"}
            },
            "required": ["nota"]
        }
    ),
    
    Tool(
        name="tiny_nota_fiscal_gerar_pedido",
        description="Gera nota fiscal a partir de um pedido",
        inputSchema={
            "type": "object",
            "properties": {
                "pedido_id": {"type": "string", "description": "ID do pedido"}
            },
            "required": ["pedido_id"]
        }
    ),
    
    Tool(
        name="tiny_nota_fiscal_enviar_email",
        description="Envia nota fiscal por email",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da nota"},
                "email": {"type": "string", "description": "Email destino"}
            },
            "required": ["id", "email"]
        }
    ),
    
    Tool(
        name="tiny_nota_fiscal_obter_xml",
        description="Obtém XML da nota fiscal",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da nota"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_nota_fiscal_cancelar",
        description="Cancela nota fiscal",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da nota"},
                "motivo": {"type": "string", "description": "Motivo do cancelamento"}
            },
            "required": ["id", "motivo"]
        }
    ),
    
    # =========================================================================
    # CONTAS A RECEBER (4 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_contas_receber_pesquisar",
        description="Pesquisa contas a receber",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1},
                "data_inicio": {"type": "string"},
                "data_fim": {"type": "string"},
                "situacao": {"type": "string"}
            }
        }
    ),
    
    Tool(
        name="tiny_conta_receber_obter",
        description="Obtém detalhes de uma conta a receber",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da conta"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_conta_receber_incluir",
        description="Cadastra nova conta a receber",
        inputSchema={
            "type": "object",
            "properties": {
                "conta": {"type": "object", "description": "Dados da conta"}
            },
            "required": ["conta"]
        }
    ),
    
    Tool(
        name="tiny_conta_receber_baixar",
        description="Baixa/Quita conta a receber",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da conta"},
                "data_pagamento": {"type": "string", "description": "Data (DD/MM/YYYY)"},
                "valor": {"type": "number", "description": "Valor pago"}
            },
            "required": ["id", "data_pagamento", "valor"]
        }
    ),
    
    # =========================================================================
    # CONTAS A PAGAR (4 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_contas_pagar_pesquisar",
        description="Pesquisa contas a pagar",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1},
                "data_inicio": {"type": "string"},
                "data_fim": {"type": "string"},
                "situacao": {"type": "string"}
            }
        }
    ),
    
    Tool(
        name="tiny_conta_pagar_obter",
        description="Obtém detalhes de uma conta a pagar",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da conta"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_conta_pagar_incluir",
        description="Cadastra nova conta a pagar",
        inputSchema={
            "type": "object",
            "properties": {
                "conta": {"type": "object", "description": "Dados da conta"}
            },
            "required": ["conta"]
        }
    ),
    
    Tool(
        name="tiny_conta_pagar_baixar",
        description="Baixa/Quita conta a pagar",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da conta"},
                "data_pagamento": {"type": "string", "description": "Data (DD/MM/YYYY)"},
                "valor": {"type": "number", "description": "Valor pago"}
            },
            "required": ["id", "data_pagamento", "valor"]
        }
    ),
    
    # =========================================================================
    # CRM / OPORTUNIDADES (4 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_crm_oportunidades_pesquisar",
        description="Pesquisa oportunidades CRM",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_crm_oportunidade_obter",
        description="Obtém detalhes de uma oportunidade",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da oportunidade"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_crm_oportunidade_incluir",
        description="Cria nova oportunidade CRM",
        inputSchema={
            "type": "object",
            "properties": {
                "oportunidade": {"type": "object", "description": "Dados da oportunidade"}
            },
            "required": ["oportunidade"]
        }
    ),
    
    Tool(
        name="tiny_crm_oportunidade_alterar",
        description="Altera oportunidade CRM",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da oportunidade"},
                "oportunidade": {"type": "object", "description": "Dados atualizados"}
            },
            "required": ["id", "oportunidade"]
        }
    ),
    
    # =========================================================================
    # COMPLEMENTARES (20+ ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_formas_pagamento_listar",
        description="Lista formas de pagamento disponíveis",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_transportadoras_pesquisar",
        description="Pesquisa transportadoras",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_transportadora_obter",
        description="Obtém detalhes de transportadora",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da transportadora"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_vendedores_pesquisar",
        description="Pesquisa vendedores",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_vendedor_obter",
        description="Obtém detalhes de vendedor",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do vendedor"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_categorias_listar",
        description="Lista categorias de produtos",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_etiquetas_listar",
        description="Lista etiquetas/tags",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_depositos_listar",
        description="Lista depósitos",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_deposito_obter_estoque",
        description="Obtém estoque de depósito",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do depósito"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_orcamentos_pesquisar",
        description="Pesquisa orçamentos",
        inputSchema={
            "type": "object",
            "properties": {
                "pesquisa": {"type": "string"},
                "pagina": {"type": "integer", "default": 1}
            },
            "required": ["pesquisa"]
        }
    ),
    
    Tool(
        name="tiny_orcamento_obter",
        description="Obtém detalhes de orçamento",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do orçamento"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_orcamento_incluir",
        description="Cria novo orçamento",
        inputSchema={
            "type": "object",
            "properties": {
                "orcamento": {"type": "object", "description": "Dados do orçamento"}
            },
            "required": ["orcamento"]
        }
    ),
    
    Tool(
        name="tiny_pedidos_compra_pesquisar",
        description="Pesquisa pedidos de compra",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_pedido_compra_obter",
        description="Obtém detalhes de pedido de compra",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do pedido"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_pedido_compra_incluir",
        description="Cria novo pedido de compra",
        inputSchema={
            "type": "object",
            "properties": {
                "pedido": {"type": "object", "description": "Dados do pedido"}
            },
            "required": ["pedido"]
        }
    ),
    
    Tool(
        name="tiny_manifestos_pesquisar",
        description="Pesquisa manifestos",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_manifesto_obter",
        description="Obtém detalhes de manifesto",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do manifesto"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_ordens_servico_pesquisar",
        description="Pesquisa ordens de serviço",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_ordem_servico_obter",
        description="Obtém detalhes de ordem de serviço",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da ordem"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_kits_pesquisar",
        description="Pesquisa kits de produtos",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_kit_obter",
        description="Obtém detalhes de kit",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do kit"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_expedicoes_pesquisar",
        description="Pesquisa expedições/entregas",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_expedicao_obter",
        description="Obtém detalhes de expedição",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da expedição"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_pdv_vendas_pesquisar",
        description="Pesquisa vendas PDV",
        inputSchema={
            "type": "object",
            "properties": {
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_pdv_venda_obter",
        description="Obtém detalhes de venda PDV",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID da venda"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_boleto_gerar",
        description="Gera boleto para conta a receber",
        inputSchema={
            "type": "object",
            "properties": {
                "conta_receber_id": {"type": "string", "description": "ID da conta"}
            },
            "required": ["conta_receber_id"]
        }
    ),
    
    Tool(
        name="tiny_boleto_obter",
        description="Obtém detalhes de boleto",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do boleto"}
            },
            "required": ["id"]
        }
    ),
    
    Tool(
        name="tiny_conta_obter_info",
        description="Obtém informações da conta/empresa",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    # =========================================================================
    # RELATÓRIOS (3 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_relatorio_vendas",
        description="Gera relatório de vendas",
        inputSchema={
            "type": "object",
            "properties": {
                "data_inicio": {"type": "string", "description": "DD/MM/YYYY"},
                "data_fim": {"type": "string", "description": "DD/MM/YYYY"},
                "tipo": {"type": "string", "default": "geral"}
            },
            "required": ["data_inicio", "data_fim"]
        }
    ),
    
    Tool(
        name="tiny_relatorio_produtos_mais_vendidos",
        description="Relatório de produtos mais vendidos",
        inputSchema={
            "type": "object",
            "properties": {
                "data_inicio": {"type": "string", "description": "DD/MM/YYYY"},
                "data_fim": {"type": "string", "description": "DD/MM/YYYY"},
                "limite": {"type": "integer", "default": 10}
            },
            "required": ["data_inicio", "data_fim"]
        }
    ),
    
    Tool(
        name="tiny_relatorio_estoque_baixo",
        description="Relatório de produtos com estoque baixo",
        inputSchema={
            "type": "object",
            "properties": {
                "minimo": {"type": "integer", "default": 5}
            }
        }
    ),
    
    # =========================================================================
    # MOVIMENTAÇÕES DE ESTOQUE (2 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_movimentacoes_estoque_pesquisar",
        description="Pesquisa movimentações de estoque",
        inputSchema={
            "type": "object",
            "properties": {
                "produto_id": {"type": "string"},
                "data_inicio": {"type": "string"},
                "data_fim": {"type": "string"},
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    Tool(
        name="tiny_movimentacao_estoque_incluir",
        description="Registra movimentação de estoque",
        inputSchema={
            "type": "object",
            "properties": {
                "movimentacao": {"type": "object", "description": "Dados da movimentação"}
            },
            "required": ["movimentacao"]
        }
    ),
    
    # =========================================================================
    # CAMPOS PERSONALIZADOS (1 ferramenta)
    # =========================================================================
    
    Tool(
        name="tiny_campos_personalizados_listar",
        description="Lista campos personalizados de um módulo",
        inputSchema={
            "type": "object",
            "properties": {
                "modulo": {"type": "string", "description": "Nome do módulo"}
            },
            "required": ["modulo"]
        }
    ),
    
    # =========================================================================
    # WEBHOOKS (3 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_webhooks_listar",
        description="Lista webhooks configurados",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_webhook_cadastrar",
        description="Cadastra novo webhook",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL do webhook"},
                "eventos": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["url", "eventos"]
        }
    ),
    
    Tool(
        name="tiny_webhook_remover",
        description="Remove webhook",
        inputSchema={
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID do webhook"}
            },
            "required": ["id"]
        }
    ),
    
    # =========================================================================
    # INTEGRAÇÕES & LOGS (3 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_integracoes_listar",
        description="Lista integrações ativas",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_logs_api_obter",
        description="Obtém logs de uso da API",
        inputSchema={
            "type": "object",
            "properties": {
                "data_inicio": {"type": "string"},
                "data_fim": {"type": "string"},
                "pagina": {"type": "integer", "default": 1}
            }
        }
    ),
    
    # =========================================================================
    # MARKETPLACE (2 ferramentas)
    # =========================================================================
    
    Tool(
        name="tiny_marketplaces_listar",
        description="Lista marketplaces integrados",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    Tool(
        name="tiny_marketplace_sincronizar",
        description="Sincroniza dados com marketplace",
        inputSchema={
            "type": "object",
            "properties": {
                "marketplace": {"type": "string", "description": "Nome do marketplace"}
            },
            "required": ["marketplace"]
        }
    ),
]


# =============================================================================
# UTILITÁRIO: MAPEAMENTO DE FERRAMENTAS
# =============================================================================

def get_all_tools() -> List[Tool]:
    """Retorna todas as ferramentas disponíveis"""
    return TOOLS_CATALOG


def get_tool_by_name(name: str) -> Tool:
    """Busca ferramenta pelo nome"""
    for tool in TOOLS_CATALOG:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool not found: {name}")


def get_tools_count() -> int:
    """Retorna quantidade total de ferramentas"""
    return len(TOOLS_CATALOG)
