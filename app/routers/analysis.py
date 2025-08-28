from fastapi import APIRouter, HTTPException, Path

# Importa os agentes de análise
from app.ia.agents.agent_risco_prazos import AgenteRiscoPrazos
from app.ia.agents.agent_proativo import gerar_insights_proativos

# Importa a nova função para buscar o texto do documento no DB de vetores
from app.ia.utils import get_full_text_by_filename

router = APIRouter(prefix="/analysis", tags=["2. Análise de Documentos"])

@router.post("/{file_name}")
def analyze_existing_document(file_name: str = Path(..., description="O nome do arquivo exato (ex: contrato_servico.pdf) que foi previamente enviado via /upload.")):
    """
    Inicia uma análise completa (riscos, prazos e insights) em um documento
    que JÁ EXISTE na base de conhecimento.
    """
    try:
        # --- ETAPA 1: Recuperar o texto completo do documento do banco de vetores ---
        print(f"Iniciando análise para o arquivo: {file_name}")
        texto_completo = get_full_text_by_filename(file_name)

        if not texto_completo:
            raise HTTPException(
                status_code=404,
                detail=f"Documento '{file_name}' não encontrado na base de dados. Verifique o nome ou faça o upload primeiro."
            )

        # --- ETAPA 2: ANÁLISE DE RISCOS E PRAZOS ---
        agente_riscos = AgenteRiscoPrazos()
        analise_riscos_prazos = agente_riscos.processar_contrato(
            texto_contrato=texto_completo,
            nome_arquivo=file_name
        )

        # --- ETAPA 3: GERAÇÃO DE INSIGHTS PROATIVOS ---
        insights_proativos = gerar_insights_proativos(texto_contrato=texto_completo)

        # --- ETAPA 4: RETORNAR RESPOSTA COMBINADA ---
        return {
            "analise_automatica": analise_riscos_prazos,
            "insights_proativos_ia": insights_proativos
        }

    except HTTPException as e:
        # Re-levanta exceções HTTP para manter o status code correto
        raise e
    except Exception as e:
        # Captura qualquer outro erro inesperado
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado durante a análise: {str(e)}")