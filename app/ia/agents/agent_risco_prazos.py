import re
from datetime import datetime, timedelta
from typing import List, Dict, Union, Tuple, Optional

# Este arquivo de configuração conteria suas palavras-chave
# Exemplo de REGRAS_RISCO em config.py:
# REGRAS_RISCO = {
#     "RESCISAO": ["rescisão", "rescindir", "cancelamento", "terminar o contrato"],
#     "MULTA": ["multa", "penalidade", "sanção"],
#     "CONFIDENCIALIDADE": ["confidencial", "sigilo", "não divulgar"],
# }
from config import REGRAS_RISCO

class AgenteRiscoPrazos:
    def __init__(self, dias_alerta_proximo: int = 30):
        """
        Inicializa o agente.
        :param dias_alerta_proximo: Número de dias para considerar um prazo como "próximo do vencimento".
        """
        self.regras_risco = REGRAS_RISCO
        self.dias_alerta_proximo = dias_alerta_proximo
        print("AgenteRiscoPrazos inicializado.")

    def processar_contrato(self, texto_contrato: str, nome_arquivo: str) -> Dict[str, Union[str, List[Dict]]]:
        """
        Processa o texto completo de um contrato para extrair riscos e prazos.
        """
        alertas_risco = []
        alertas_prazo = []

        # 1. Divide o texto em sentenças de forma mais inteligente
        sentencas = re.split(r'(?<=[.!?])\s+', texto_contrato)
        print(f"Contrato '{nome_arquivo}' dividido em {len(sentencas)} sentenças para análise.")

        # 2. Itera sobre cada sentença para análise individual
        for sentenca in sentencas:
            if not sentenca.strip():
                continue

            # Extrai riscos da sentença
            riscos_encontrados = self._classificar_risco(sentenca)
            if riscos_encontrados:
                for risco in riscos_encontrados:
                    alertas_risco.append({
                        "tipo_risco": risco,
                        "fonte": sentenca.strip(),
                        "confianca": 0.9 # Placeholder para futura lógica de confiança
                    })

            # Extrai prazos da sentença
            prazo_encontrado = self._extrair_prazo(sentenca)
            if prazo_encontrado:
                data_limite, evento = prazo_encontrado
                status, dias_restantes = self._get_status_prazo(data_limite)
                
                alertas_prazo.append({
                    "evento": evento,
                    "deadline": data_limite.isoformat(),
                    "status": status,
                    "dias_restantes": dias_restantes,
                    "fonte": sentenca.strip()
                })
        
        # 3. Ordena os prazos por data (do mais antigo para o mais novo)
        alertas_prazo_ordenados = sorted(alertas_prazo, key=lambda p: p['deadline'])

        return {
            "nome_arquivo": nome_arquivo,
            "alertas_risco": alertas_risco,
            "alertas_prazo": alertas_prazo_ordenados
        }

    def _classificar_risco(self, texto: str) -> List[str]:
        """Verifica uma sentença e retorna uma lista de todos os tipos de risco encontrados."""
        riscos = []
        texto_lower = texto.lower()
        for tipo, palavras_chave in self.regras_risco.items():
            if any(palavra in texto_lower for palavra in palavras_chave):
                riscos.append(tipo)
        return riscos

    def _get_status_prazo(self, data_limite: datetime) -> Tuple[str, int]:
        """Determina o status de um prazo (Vencido, Alerta Próximo, OK)."""
        hoje = datetime.now()
        diferenca = (data_limite - hoje).days

        if diferenca < 0:
            return "Vencido", diferenca
        elif diferenca <= self.dias_alerta_proximo:
            return "Alerta Próximo", diferenca
        else:
            return "OK", diferenca

    def _extrair_prazo(self, texto: str) -> Optional[Tuple[datetime, str]]:
        """Extrai a primeira data ou prazo encontrado em uma sentença."""
        texto_lower = texto.lower()
        data_referencia = datetime.now()

        # Padrão 1: "em até XX dias/meses (úteis/corridos)"
        match = re.search(r'em até (\d+)\s*(?:\(.*\))?\s*(dias|meses)\s*(úteis|corridos)?', texto_lower)
        if match:
            quantidade = int(match.group(1))
            unidade = match.group(2)
            tipo_dias = match.group(3) if match.group(3) else "corridos"

            if unidade == "meses":
                data_limite = data_referencia + timedelta(days=quantidade * 30)
                evento = f"Prazo de {quantidade} meses"
            else: # dias
                if tipo_dias == "úteis":
                    data_limite = self._calcular_data_util(data_referencia, quantidade)
                    evento = f"Prazo de {quantidade} dias úteis"
                else:
                    data_limite = data_referencia + timedelta(days=quantidade)
                    evento = f"Prazo de {quantidade} dias corridos"
            return data_limite, evento

        # Padrão 2: "até o dia DD de MM de YYYY"
        match_data = re.search(r'até (?:o dia )?(\d{1,2}) de (\w+) de (\d{4})', texto_lower)
        if match_data:
            dia, mes_str, ano = match_data.groups()
            meses = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
                'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            mes = meses.get(mes_str)
            if mes:
                data_limite = datetime(int(ano), mes, int(dia))
                evento = f"Data limite em {dia}/{mes}/{ano}"
                return data_limite, evento

        return None

    def _calcular_data_util(self, data_inicial: datetime, dias: int) -> datetime:
        """Calcula uma data futura considerando apenas dias úteis (Seg-Sex)."""
        dias_adicionados = 0
        data_atual = data_inicial
        while dias_adicionados < dias:
            data_atual += timedelta(days=1)
            if data_atual.weekday() < 5: # 0=Segunda, 4=Sexta
                dias_adicionados += 1
        return data_atual

# --- Exemplo de como usar o agente ---
if __name__ == '__main__':
    # Simula o texto de um contrato
    texto_exemplo = """
    Este contrato de confidencialidade tem validade de 24 meses.
    A parte infratora deverá pagar uma multa em até 30 dias corridos após a notificação.
    O acordo pode ser terminado por qualquer uma das partes.
    O pagamento final deve ser realizado até o dia 15 de setembro de 2025.
    Qualquer notificação de rescisão deve ser enviada com 15 dias úteis de antecedência.
    Um relatório de performance deve ser entregue até o dia 25 de agosto de 2025, o que já passou.
    """

    agente = AgenteRiscoPrazos(dias_alerta_proximo=30)
    resultado = agente.processar_contrato(texto_contrato=texto_exemplo, nome_arquivo="contrato_exemplo.pdf")

    import json
    # Imprime o resultado de forma legível
    print(json.dumps(resultado, indent=4, default=str))