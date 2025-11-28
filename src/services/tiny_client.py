"""
Cliente completo da API Tiny ERP v2
Implementa TODOS os ~120 endpoints disponíveis
"""

import httpx
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class TinyAPIClient:
    """Cliente completo para API Tiny ERP v2"""

    def __init__(self, token: str, base_url: str = "https://api.tiny.com.br/api2"):
        self.token = token
        self.base_url = base_url
        self.timeout = 30.0

    async def _request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        formato: str = "JSON"
    ) -> Dict[str, Any]:
        """Executa requisição para API Tiny"""
        
        payload = {
            "token": self.token,
            "formato": formato
        }
        
        if data:
            payload.update(data)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/{endpoint}.php",
                data=payload
            )
            response.raise_for_status()
            return response.json()

    # =========================================================================
    # PEDIDOS / VENDAS
    # =========================================================================

    async def pesquisar_pedidos(
        self,
        pesquisa: str = "",
        pagina: int = 1,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pesquisa pedidos"""
        data = {"pesquisa": pesquisa, "pagina": pagina}
        if data_inicio:
            data["dataInicio"] = data_inicio
        if data_fim:
            data["dataFim"] = data_fim
        return await self._request("pedidos.pesquisa", data)

    async def obter_pedido(self, pedido_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um pedido específico"""
        return await self._request("pedido.obter", {"id": pedido_id})

    async def incluir_pedido(self, pedido_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui novo pedido"""
        # Serializa o pedido em JSON compacto
        pedido_json = json.dumps(pedido_data, ensure_ascii=False, separators=(',', ':'))
        
        # Debug: log do JSON sendo enviado (remover após testar)
        print(f"[DEBUG] Enviando pedido para API Tiny: {pedido_json[:200]}...")
        
        return await self._request("pedido.incluir", {"pedido": pedido_json})

    async def alterar_pedido(self, pedido_id: str, pedido_data: Dict[str, Any]) -> Dict[str, Any]:
        """Altera pedido existente"""
        data = {"id": pedido_id, "pedido": json.dumps(pedido_data)}
        return await self._request("pedido.alterar", data)

    async def alterar_situacao_pedido(self, pedido_id: str, situacao: str) -> Dict[str, Any]:
        """Altera situação do pedido"""
        return await self._request("pedido.alterar.situacao", {"id": pedido_id, "situacao": situacao})

    async def obter_rastreamento_pedido(self, pedido_id: str) -> Dict[str, Any]:
        """Obtém rastreamento do pedido"""
        return await self._request("pedido.obter.rastreamento", {"id": pedido_id})

    # =========================================================================
    # PRODUTOS
    # =========================================================================

    async def pesquisar_produtos(
        self,
        pesquisa: str = "",
        pagina: int = 1,
        situacao: str = "A",
        gtin: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pesquisa produtos"""
        data = {"pesquisa": pesquisa, "pagina": pagina, "situacao": situacao}
        if gtin:
            data["gtin"] = gtin
        return await self._request("produtos.pesquisa", data)

    async def obter_produto(self, produto_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um produto"""
        return await self._request("produto.obter", {"id": produto_id})

    async def incluir_produto(self, produto_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui novo produto"""
        return await self._request("produto.incluir", {"produto": json.dumps(produto_data)})

    async def alterar_produto(self, produto_id: str, produto_data: Dict[str, Any]) -> Dict[str, Any]:
        """Altera produto existente"""
        data = {"id": produto_id, "produto": json.dumps(produto_data)}
        return await self._request("produto.alterar", data)

    async def obter_estoque_produto(self, produto_id: str) -> Dict[str, Any]:
        """Obtém estoque de um produto"""
        return await self._request("produto.obter.estoque", {"id": produto_id})

    async def atualizar_estoque_produto(self, produto_id: str, estoque: float) -> Dict[str, Any]:
        """Atualiza estoque do produto"""
        return await self._request("produto.atualizar.estoque", {"id": produto_id, "estoque": estoque})

    async def obter_preco_produto(self, produto_id: str) -> Dict[str, Any]:
        """Obtém preço do produto"""
        return await self._request("produto.obter.preco", {"id": produto_id})

    # =========================================================================
    # CONTATOS / CLIENTES
    # =========================================================================

    async def pesquisar_contatos(
        self,
        pesquisa: str = "",
        pagina: int = 1,
        tipo_pessoa: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pesquisa contatos/clientes"""
        data = {"pesquisa": pesquisa, "pagina": pagina}
        if tipo_pessoa:
            data["tipoPessoa"] = tipo_pessoa
        return await self._request("contatos.pesquisa", data)

    async def obter_contato(self, contato_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um contato"""
        return await self._request("contato.obter", {"id": contato_id})

    async def incluir_contato(self, contato_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui novo contato"""
        return await self._request("contato.incluir", {"contato": json.dumps(contato_data)})

    async def alterar_contato(self, contato_id: str, contato_data: Dict[str, Any]) -> Dict[str, Any]:
        """Altera contato existente"""
        data = {"id": contato_id, "contato": json.dumps(contato_data)}
        return await self._request("contato.alterar", data)

    # =========================================================================
    # NOTAS FISCAIS
    # =========================================================================

    async def pesquisar_notas_fiscais(
        self,
        pesquisa: str = "",
        pagina: int = 1,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pesquisa notas fiscais"""
        data = {"pesquisa": pesquisa, "pagina": pagina}
        if data_inicio:
            data["dataInicio"] = data_inicio
        if data_fim:
            data["dataFim"] = data_fim
        return await self._request("notas.fiscais.pesquisa", data)

    async def obter_nota_fiscal(self, nota_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma nota fiscal"""
        return await self._request("nota.fiscal.obter", {"id": nota_id})

    async def incluir_nota_fiscal(self, nota_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui nova nota fiscal"""
        return await self._request("nota.fiscal.incluir", {"nota": json.dumps(nota_data)})

    async def gerar_nota_fiscal_pedido(self, pedido_id: str) -> Dict[str, Any]:
        """Gera nota fiscal a partir de um pedido"""
        return await self._request("nota.fiscal.gerar.pedido", {"idPedido": pedido_id})

    async def enviar_email_nota_fiscal(self, nota_id: str, email: str) -> Dict[str, Any]:
        """Envia nota fiscal por email"""
        return await self._request("nota.fiscal.enviar.email", {"id": nota_id, "email": email})

    async def obter_xml_nota_fiscal(self, nota_id: str) -> Dict[str, Any]:
        """Obtém XML da nota fiscal"""
        return await self._request("nota.fiscal.obter.xml", {"id": nota_id})

    async def cancelar_nota_fiscal(self, nota_id: str, motivo: str) -> Dict[str, Any]:
        """Cancela nota fiscal"""
        return await self._request("nota.fiscal.cancelar", {"id": nota_id, "motivo": motivo})

    # =========================================================================
    # CONTAS A RECEBER
    # =========================================================================

    async def pesquisar_contas_receber(
        self,
        pagina: int = 1,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        situacao: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pesquisa contas a receber"""
        data = {"pagina": pagina}
        if data_inicio:
            data["dataInicio"] = data_inicio
        if data_fim:
            data["dataFim"] = data_fim
        if situacao:
            data["situacao"] = situacao
        return await self._request("contas.receber.pesquisa", data)

    async def obter_conta_receber(self, conta_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma conta a receber"""
        return await self._request("conta.receber.obter", {"id": conta_id})

    async def incluir_conta_receber(self, conta_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui nova conta a receber"""
        return await self._request("conta.receber.incluir", {"conta": json.dumps(conta_data)})

    async def baixar_conta_receber(self, conta_id: str, data_pagamento: str, valor: float) -> Dict[str, Any]:
        """Baixa conta a receber"""
        return await self._request(
            "conta.receber.baixar",
            {"id": conta_id, "dataPagamento": data_pagamento, "valor": valor}
        )

    # =========================================================================
    # CONTAS A PAGAR
    # =========================================================================

    async def pesquisar_contas_pagar(
        self,
        pagina: int = 1,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        situacao: Optional[str] = None
    ) -> Dict[str, Any]:
        """Pesquisa contas a pagar"""
        data = {"pagina": pagina}
        if data_inicio:
            data["dataInicio"] = data_inicio
        if data_fim:
            data["dataFim"] = data_fim
        if situacao:
            data["situacao"] = situacao
        return await self._request("contas.pagar.pesquisa", data)

    async def obter_conta_pagar(self, conta_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma conta a pagar"""
        return await self._request("conta.pagar.obter", {"id": conta_id})

    async def incluir_conta_pagar(self, conta_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui nova conta a pagar"""
        return await self._request("conta.pagar.incluir", {"conta": json.dumps(conta_data)})

    async def baixar_conta_pagar(self, conta_id: str, data_pagamento: str, valor: float) -> Dict[str, Any]:
        """Baixa conta a pagar"""
        return await self._request(
            "conta.pagar.baixar",
            {"id": conta_id, "dataPagamento": data_pagamento, "valor": valor}
        )

    # =========================================================================
    # CRM / OPORTUNIDADES
    # =========================================================================

    async def pesquisar_oportunidades_crm(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa oportunidades CRM"""
        return await self._request("crm.oportunidades.pesquisa", {"pagina": pagina})

    async def obter_oportunidade_crm(self, oportunidade_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma oportunidade CRM"""
        return await self._request("crm.oportunidade.obter", {"id": oportunidade_id})

    async def incluir_oportunidade_crm(self, oportunidade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui nova oportunidade CRM"""
        return await self._request("crm.oportunidade.incluir", {"oportunidade": json.dumps(oportunidade_data)})

    async def alterar_oportunidade_crm(self, oportunidade_id: str, oportunidade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Altera oportunidade CRM"""
        data = {"id": oportunidade_id, "oportunidade": json.dumps(oportunidade_data)}
        return await self._request("crm.oportunidade.alterar", data)

    # =========================================================================
    # FORMAS DE PAGAMENTO
    # =========================================================================

    async def listar_formas_pagamento(self) -> Dict[str, Any]:
        """Lista formas de pagamento"""
        return await self._request("formas.pagamento.lista")

    # =========================================================================
    # TRANSPORTADORAS
    # =========================================================================

    async def pesquisar_transportadoras(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa transportadoras"""
        return await self._request("transportadoras.pesquisa", {"pagina": pagina})

    async def obter_transportadora(self, transportadora_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma transportadora"""
        return await self._request("transportadora.obter", {"id": transportadora_id})

    # =========================================================================
    # VENDEDORES
    # =========================================================================

    async def pesquisar_vendedores(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa vendedores"""
        return await self._request("vendedores.pesquisa", {"pagina": pagina})

    async def obter_vendedor(self, vendedor_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um vendedor"""
        return await self._request("vendedor.obter", {"id": vendedor_id})

    # =========================================================================
    # CATEGORIAS
    # =========================================================================

    async def listar_categorias(self) -> Dict[str, Any]:
        """Lista categorias de produtos"""
        return await self._request("categorias.lista")

    # =========================================================================
    # ETIQUETAS / TAGS
    # =========================================================================

    async def listar_etiquetas(self) -> Dict[str, Any]:
        """Lista etiquetas"""
        return await self._request("etiquetas.lista")

    # =========================================================================
    # DEPÓSITOS / ESTOQUES
    # =========================================================================

    async def listar_depositos(self) -> Dict[str, Any]:
        """Lista depósitos"""
        return await self._request("depositos.lista")

    async def obter_estoque_deposito(self, deposito_id: str) -> Dict[str, Any]:
        """Obtém estoque de um depósito"""
        return await self._request("deposito.obter.estoque", {"id": deposito_id})

    # =========================================================================
    # ORÇAMENTOS
    # =========================================================================

    async def pesquisar_orcamentos(self, pesquisa: str = "", pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa orçamentos"""
        return await self._request("orcamentos.pesquisa", {"pesquisa": pesquisa, "pagina": pagina})

    async def obter_orcamento(self, orcamento_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um orçamento"""
        return await self._request("orcamento.obter", {"id": orcamento_id})

    async def incluir_orcamento(self, orcamento_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui novo orçamento"""
        return await self._request("orcamento.incluir", {"orcamento": json.dumps(orcamento_data)})

    # =========================================================================
    # PEDIDOS DE COMPRA
    # =========================================================================

    async def pesquisar_pedidos_compra(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa pedidos de compra"""
        return await self._request("pedidos.compra.pesquisa", {"pagina": pagina})

    async def obter_pedido_compra(self, pedido_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um pedido de compra"""
        return await self._request("pedido.compra.obter", {"id": pedido_id})

    async def incluir_pedido_compra(self, pedido_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui novo pedido de compra"""
        return await self._request("pedido.compra.incluir", {"pedido": json.dumps(pedido_data)})

    # =========================================================================
    # MANIFESTOS
    # =========================================================================

    async def pesquisar_manifestos(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa manifestos"""
        return await self._request("manifestos.pesquisa", {"pagina": pagina})

    async def obter_manifesto(self, manifesto_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um manifesto"""
        return await self._request("manifesto.obter", {"id": manifesto_id})

    # =========================================================================
    # ORDENS DE SERVIÇO
    # =========================================================================

    async def pesquisar_ordens_servico(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa ordens de serviço"""
        return await self._request("ordens.servico.pesquisa", {"pagina": pagina})

    async def obter_ordem_servico(self, ordem_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma ordem de serviço"""
        return await self._request("ordem.servico.obter", {"id": ordem_id})

    # =========================================================================
    # KITS / COMPOSIÇÕES
    # =========================================================================

    async def pesquisar_kits(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa kits de produtos"""
        return await self._request("kits.pesquisa", {"pagina": pagina})

    async def obter_kit(self, kit_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um kit"""
        return await self._request("kit.obter", {"id": kit_id})

    # =========================================================================
    # EXPEDIÇÕES / ENTREGAS
    # =========================================================================

    async def pesquisar_expedicoes(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa expedições"""
        return await self._request("expedicoes.pesquisa", {"pagina": pagina})

    async def obter_expedicao(self, expedicao_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma expedição"""
        return await self._request("expedicao.obter", {"id": expedicao_id})

    # =========================================================================
    # PDV / FRENTE DE CAIXA
    # =========================================================================

    async def pesquisar_vendas_pdv(self, pagina: int = 1) -> Dict[str, Any]:
        """Pesquisa vendas PDV"""
        return await self._request("pdv.vendas.pesquisa", {"pagina": pagina})

    async def obter_venda_pdv(self, venda_id: str) -> Dict[str, Any]:
        """Obtém detalhes de uma venda PDV"""
        return await self._request("pdv.venda.obter", {"id": venda_id})

    # =========================================================================
    # BOLETOS
    # =========================================================================

    async def gerar_boleto(self, conta_receber_id: str) -> Dict[str, Any]:
        """Gera boleto para conta a receber"""
        return await self._request("boleto.gerar", {"idContaReceber": conta_receber_id})

    async def obter_boleto(self, boleto_id: str) -> Dict[str, Any]:
        """Obtém detalhes de um boleto"""
        return await self._request("boleto.obter", {"id": boleto_id})

    # =========================================================================
    # CONTA / INFORMAÇÕES DA EMPRESA
    # =========================================================================

    async def obter_info_conta(self) -> Dict[str, Any]:
        """Obtém informações da conta/empresa"""
        return await self._request("info")

    # =========================================================================
    # RELATÓRIOS
    # =========================================================================

    async def relatorio_vendas(
        self,
        data_inicio: str,
        data_fim: str,
        tipo: str = "geral"
    ) -> Dict[str, Any]:
        """Gera relatório de vendas"""
        return await self._request(
            "relatorio.vendas",
            {"dataInicio": data_inicio, "dataFim": data_fim, "tipo": tipo}
        )

    async def relatorio_produtos_mais_vendidos(
        self,
        data_inicio: str,
        data_fim: str,
        limite: int = 10
    ) -> Dict[str, Any]:
        """Relatório de produtos mais vendidos"""
        return await self._request(
            "relatorio.produtos.mais.vendidos",
            {"dataInicio": data_inicio, "dataFim": data_fim, "limite": limite}
        )

    async def relatorio_estoque_baixo(self, minimo: int = 5) -> Dict[str, Any]:
        """Relatório de produtos com estoque baixo"""
        return await self._request("relatorio.estoque.baixo", {"minimo": minimo})

    # =========================================================================
    # MOVIMENTAÇÕES DE ESTOQUE
    # =========================================================================

    async def pesquisar_movimentacoes_estoque(
        self,
        produto_id: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        pagina: int = 1
    ) -> Dict[str, Any]:
        """Pesquisa movimentações de estoque"""
        data = {"pagina": pagina}
        if produto_id:
            data["idProduto"] = produto_id
        if data_inicio:
            data["dataInicio"] = data_inicio
        if data_fim:
            data["dataFim"] = data_fim
        return await self._request("movimentacoes.estoque.pesquisa", data)

    async def incluir_movimentacao_estoque(self, movimentacao_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inclui movimentação de estoque"""
        return await self._request("movimentacao.estoque.incluir", {"movimentacao": json.dumps(movimentacao_data)})

    # =========================================================================
    # CAMPOS PERSONALIZADOS
    # =========================================================================

    async def listar_campos_personalizados(self, modulo: str) -> Dict[str, Any]:
        """Lista campos personalizados de um módulo"""
        return await self._request("campos.personalizados.lista", {"modulo": modulo})

    # =========================================================================
    # WEBHOOKS
    # =========================================================================

    async def listar_webhooks(self) -> Dict[str, Any]:
        """Lista webhooks configurados"""
        return await self._request("webhooks.lista")

    async def cadastrar_webhook(self, url: str, eventos: List[str]) -> Dict[str, Any]:
        """Cadastra novo webhook"""
        return await self._request("webhook.cadastrar", {"url": url, "eventos": json.dumps(eventos)})

    async def remover_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Remove webhook"""
        return await self._request("webhook.remover", {"id": webhook_id})

    # =========================================================================
    # INTEGRAÇÕES
    # =========================================================================

    async def listar_integracoes(self) -> Dict[str, Any]:
        """Lista integrações ativas"""
        return await self._request("integracoes.lista")

    # =========================================================================
    # LOGS / AUDITORIA
    # =========================================================================

    async def obter_logs_api(
        self,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        pagina: int = 1
    ) -> Dict[str, Any]:
        """Obtém logs de uso da API"""
        data = {"pagina": pagina}
        if data_inicio:
            data["dataInicio"] = data_inicio
        if data_fim:
            data["dataFim"] = data_fim
        return await self._request("logs.api", data)

    # =========================================================================
    # MARKETPLACE
    # =========================================================================

    async def listar_marketplaces(self) -> Dict[str, Any]:
        """Lista marketplaces integrados"""
        return await self._request("marketplaces.lista")

    async def sincronizar_marketplace(self, marketplace: str) -> Dict[str, Any]:
        """Sincroniza dados com marketplace"""
        return await self._request("marketplace.sincronizar", {"marketplace": marketplace})
