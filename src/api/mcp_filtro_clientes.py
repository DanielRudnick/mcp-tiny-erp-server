"""
Ferramenta MCP para buscar clientes no CSV exportado do Tiny
Busca inteligente por CPF, Email ou Telefone
"""
import csv
import re
from typing import Dict, Any, Optional, List

class ClienteFiltroCSV:
    """Filtro inteligente de clientes usando CSV exportado"""
    
    def __init__(self, csv_path: str = "/mnt/user-data/uploads/contatos_teste.csv"):
        self.csv_path = csv_path
        self.clientes = []
        self._carregar_csv()
    
    def _carregar_csv(self):
        """Carrega CSV e prepara dados"""
        try:
            with open(self.csv_path, 'r', encoding='latin-1') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    cliente = {
                        'id': row.get('ID', ''),
                        'nome': row.get('Nome', ''),
                        'cpf_cnpj': row.get('CNPJ / CPF', ''),
                        'email': row.get('E-mail', ''),
                        'celular': row.get('Celular', ''),
                        'fone': row.get('Fone', ''),
                        'cidade': row.get('Cidade', ''),
                        'estado': row.get('Estado', '')
                    }
                    self.clientes.append(cliente)
            print(f"✅ CSV carregado: {len(self.clientes)} clientes")
        except Exception as e:
            print(f"❌ Erro ao carregar CSV: {e}")
    
    def _limpar_cpf_cnpj(self, valor: str) -> str:
        """Remove formatação de CPF/CNPJ"""
        if not valor:
            return ""
        # Remove tudo que não é número
        return re.sub(r'[^\d]', '', valor)
    
    def _limpar_telefone(self, valor: str) -> str:
        """Remove formatação de telefone"""
        if not valor:
            return ""
        # Remove tudo que não é número
        return re.sub(r'[^\d]', '', valor)
    
    def _limpar_email(self, valor: str) -> str:
        """Normaliza email"""
        if not valor:
            return ""
        return valor.lower().strip()
    
    def buscar_por_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """Busca cliente por CPF (com ou sem formatação)"""
        cpf_limpo = self._limpar_cpf_cnpj(cpf)
        
        for cliente in self.clientes:
            cpf_cliente = self._limpar_cpf_cnpj(cliente['cpf_cnpj'])
            if cpf_cliente == cpf_limpo and len(cpf_limpo) == 11:  # CPF tem 11 dígitos
                return cliente
        
        return None
    
    def buscar_por_cnpj(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """Busca cliente por CNPJ (com ou sem formatação)"""
        cnpj_limpo = self._limpar_cpf_cnpj(cnpj)
        
        for cliente in self.clientes:
            cnpj_cliente = self._limpar_cpf_cnpj(cliente['cpf_cnpj'])
            if cnpj_cliente == cnpj_limpo and len(cnpj_limpo) == 14:  # CNPJ tem 14 dígitos
                return cliente
        
        return None
    
    def buscar_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca cliente por email"""
        email_limpo = self._limpar_email(email)
        
        for cliente in self.clientes:
            email_cliente = self._limpar_email(cliente['email'])
            if email_cliente == email_limpo and email_limpo:
                return cliente
        
        return None
    
    def buscar_por_telefone(self, telefone: str) -> List[Dict[str, Any]]:
        """Busca cliente por telefone (celular ou fone)"""
        telefone_limpo = self._limpar_telefone(telefone)
        resultados = []
        
        # Precisa ter pelo menos 8 dígitos
        if len(telefone_limpo) < 8:
            return resultados
        
        for cliente in self.clientes:
            celular_limpo = self._limpar_telefone(cliente['celular'])
            fone_limpo = self._limpar_telefone(cliente['fone'])
            
            # Busca pelos últimos dígitos (mais flexível)
            if (telefone_limpo in celular_limpo or 
                telefone_limpo in fone_limpo or
                celular_limpo.endswith(telefone_limpo[-8:]) or  # Últimos 8 dígitos
                fone_limpo.endswith(telefone_limpo[-8:])):
                resultados.append(cliente)
        
        return resultados
    
    def buscar_inteligente(self, dado: str) -> Dict[str, Any]:
        """
        Busca inteligente: detecta automaticamente o tipo
        Retorna o nome do cliente para usar no tiny_contatos_pesquisar
        """
        dado = dado.strip()
        
        # Detecta tipo automaticamente
        dado_limpo = self._limpar_cpf_cnpj(dado)
        
        # CPF (11 dígitos)
        if len(dado_limpo) == 11 and dado_limpo.isdigit():
            cliente = self.buscar_por_cpf(dado)
            if cliente:
                return {
                    "encontrado": True,
                    "tipo": "cpf",
                    "nome": cliente['nome'],
                    "cpf_cnpj": cliente['cpf_cnpj'],
                    "email": cliente['email'],
                    "telefone": cliente['celular'] or cliente['fone'],
                    "cidade": cliente['cidade'],
                    "estado": cliente['estado']
                }
        
        # CNPJ (14 dígitos)
        elif len(dado_limpo) == 14 and dado_limpo.isdigit():
            cliente = self.buscar_por_cnpj(dado)
            if cliente:
                return {
                    "encontrado": True,
                    "tipo": "cnpj",
                    "nome": cliente['nome'],
                    "cpf_cnpj": cliente['cpf_cnpj'],
                    "email": cliente['email'],
                    "telefone": cliente['celular'] or cliente['fone'],
                    "cidade": cliente['cidade'],
                    "estado": cliente['estado']
                }
        
        # Email (tem @)
        elif '@' in dado:
            cliente = self.buscar_por_email(dado)
            if cliente:
                return {
                    "encontrado": True,
                    "tipo": "email",
                    "nome": cliente['nome'],
                    "cpf_cnpj": cliente['cpf_cnpj'],
                    "email": cliente['email'],
                    "telefone": cliente['celular'] or cliente['fone'],
                    "cidade": cliente['cidade'],
                    "estado": cliente['estado']
                }
        
        # Telefone (só números ou com formatação)
        elif len(dado_limpo) >= 8:
            clientes = self.buscar_por_telefone(dado)
            if len(clientes) == 1:
                cliente = clientes[0]
                return {
                    "encontrado": True,
                    "tipo": "telefone",
                    "nome": cliente['nome'],
                    "cpf_cnpj": cliente['cpf_cnpj'],
                    "email": cliente['email'],
                    "telefone": cliente['celular'] or cliente['fone'],
                    "cidade": cliente['cidade'],
                    "estado": cliente['estado']
                }
            elif len(clientes) > 1:
                return {
                    "encontrado": True,
                    "tipo": "telefone",
                    "multiplos": True,
                    "total": len(clientes),
                    "clientes": [
                        {
                            "nome": c['nome'],
                            "telefone": c['celular'] or c['fone'],
                            "cidade": c['cidade']
                        }
                        for c in clientes[:5]  # Máximo 5
                    ],
                    "mensagem": f"Encontrei {len(clientes)} clientes com esse telefone. Por favor, informe CPF ou email para identificar."
                }
        
        # Não encontrou
        return {
            "encontrado": False,
            "tipo": "desconhecido",
            "mensagem": "Cliente não encontrado no cadastro. Posso criar um novo cadastro para você?"
        }


# =============================================================================
# TOOL MCP
# =============================================================================

async def mcp_filtro_clientes_excel(
    dado: str
) -> Dict[str, Any]:
    """
    Busca inteligente de cliente no CSV exportado
    Detecta automaticamente se é CPF, CNPJ, Email ou Telefone
    Retorna o NOME para usar no tiny_contatos_pesquisar
    
    Args:
        dado: CPF, CNPJ, Email ou Telefone do cliente
    
    Returns:
        {
            "encontrado": true,
            "nome": "João Silva",
            "cpf_cnpj": "123.456.789-00",
            "email": "joao@email.com",
            "telefone": "(11) 99999-9999",
            "cidade": "São Paulo",
            "estado": "SP"
        }
    """
    try:
        filtro = ClienteFiltroCSV()
        resultado = filtro.buscar_inteligente(dado)
        return resultado
    except Exception as e:
        return {
            "encontrado": False,
            "erro": str(e),
            "mensagem": "Erro ao buscar cliente no CSV"
        }


# =============================================================================
# EXEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def testar():
        # Teste CPF sem formatação
        print("\n=== TESTE 1: CPF sem formatação ===")
        resultado = await mcp_filtro_clientes_excel("11283871904")
        print(resultado)
        
        # Teste CPF com formatação
        print("\n=== TESTE 2: CPF com formatação ===")
        resultado = await mcp_filtro_clientes_excel("112.838.719-04")
        print(resultado)
        
        # Teste Email
        print("\n=== TESTE 3: Email ===")
        resultado = await mcp_filtro_clientes_excel("d.rudnick.dr@gmail.com")
        print(resultado)
        
        # Teste telefone
        print("\n=== TESTE 4: Telefone ===")
        resultado = await mcp_filtro_clientes_excel("11951072887")
        print(resultado)
        
        # Teste não encontrado
        print("\n=== TESTE 5: Não encontrado ===")
        resultado = await mcp_filtro_clientes_excel("99999999999")
        print(resultado)
    
    asyncio.run(testar())
