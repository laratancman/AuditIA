# AuditIA/app/ia/agents/agente_risco_prazos/risco_prazos.py

import json
import re
from datetime import datetime, timedelta

from AuditIA.config import REGRAS_RISCO

class AgenteRiscoPrazos:
    def __init__(self):
        print("AgenteRiscoPrazos inicializado.")
        self.regras_risco = REGRAS_RISCO
        print(f"Regras de risco carregadas: {len(self.regras_risco)} tipos.")

    # *** O MÉTODO ABAIXO FOI SIGNIFICATIVAMENTE ALTERADO ***
    def processar(self, dados_de_entrada):
        """
        Este método agora recebe um texto completo, o divide em sentenças
        e analisa cada uma delas em busca de múltiplos alertas.
        """
        alertas_finais = []
        
        # Esperamos que a entrada seja uma lista com um dicionário contendo o texto completo.
        texto_completo = dados_de_entrada[0].get("texto", "")

        # 1. Dividimos o texto completo em sentenças. Usamos o ponto final como separador.
        # O `if s.strip()` garante que não teremos sentenças vazias na lista.
        sentencas = [s.strip() for s in texto_completo.split('.') if s.strip()]

        print(f"[AgenteRiscoPrazos] O texto foi dividido em {len(sentencas)} sentenças para análise.")

        # 2. Agora, iteramos sobre cada sentença encontrada
        for sentenca in sentencas:
            # Para cada sentença, buscamos por um tipo de risco e um prazo
            tipo_risco = self._classificar_risco(sentenca)
            data_limite, evento = self._extrair_prazo(sentenca)

            # 3. Se encontrarmos um risco OU um prazo na sentença, criamos um alerta
            if tipo_risco or data_limite:
                alerta = {
                    "tipo_risco": tipo_risco,
                    "evento": evento,
                    "deadline": data_limite.isoformat() if data_limite else None,
                    "fonte": sentenca + ".", # Adicionamos o ponto de volta para contexto
                    "confianca": 0.9 # Podemos ajustar a confiança depois
                }
                alertas_finais.append(alerta)
        
        return {"alertas": alertas_finais}

    def _classificar_risco(self, texto):
        texto_lower = texto.lower()
        for tipo, palavras_chave in self.regras_risco.items():
            for palavra in palavras_chave:
                if palavra in texto_lower:
                    return tipo
        return None

    def _calcular_data_util(self, data_inicial, dias):
        dias_adicionados = 0
        data_atual = data_inicial
        while dias_adicionados < dias:
            data_atual += timedelta(days=1)
            if data_atual.weekday() < 5:
                dias_adicionados += 1
        return data_atual

    def _extrair_prazo(self, texto):
        texto_lower = texto.lower()
        data_referencia = datetime.now()
        match_dias = re.search(r'em até (\d+)\s*(\(.*\))?\s*dias\s*(úteis|corridos)?', texto_lower)
        if match_dias:
            quantidade_dias = int(match_dias.group(1))
            tipo_dias = match_dias.group(3) if match_dias.group(3) else "corridos"
            if tipo_dias == "úteis":
                data_limite = self._calcular_data_util(data_referencia, quantidade_dias)
                evento_prazo = f"Prazo: {quantidade_dias} dias úteis"
            else:
                data_limite = data_referencia + timedelta(days=quantidade_dias)
                evento_prazo = f"Prazo: {quantidade_dias} dias corridos"
            return data_limite, evento_prazo
        match_meses = re.search(r'em até (\d+)\s+meses', texto_lower)
        if match_meses:
            quantidade_meses = int(match_meses.group(1))
            data_limite = data_referencia + timedelta(days=quantidade_meses * 30)
            return data_limite, f"Prazo: {quantidade_meses} meses"
        return None, None