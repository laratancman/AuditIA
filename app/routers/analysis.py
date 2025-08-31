from fastapi import APIRouter, HTTPException, Path

from app.ia.agents.agent_risco_prazos import AgenteRiscoPrazos
from app.ia.agents.agent_proativo import gerar_insights_proativos
from app.ia.utils import get_full_text_by_filename

router = APIRouter(prefix="/analysis", tags=["2. Análise de Documentos"])

@router.post("/{file_name}")
def analyze_existing_document(file_name: str = Path(..., description="O nome do arquivo exato (ex: contrato_servico.pdf) que foi previamente enviado via /upload.")):
    """
    Inicia uma análise completa (riscos, prazos e insights) em um documento
    que JÁ EXISTE na base de conhecimento.
    """
    
    # --- LINHA DE DEPURAÇÃO ADICIONADA ---
    # Isto irá imprimir no terminal do backend o nome EXATO do arquivo que o frontend enviou.
    print(f"--- DEBUG: Rota de análise recebida para o arquivo: '{file_name}' ---")
    
    try:
        # O resto do seu código continua igual...
        print(f"Iniciando análise para o arquivo: {file_name}")
        texto_completo = get_full_text_by_filename(file_name)

        if not texto_completo:
            raise HTTPException(
                status_code=404,
                detail=f"Documento '{file_name}' não encontrado na base de dados. Verifique o nome ou faça o upload primeiro."
            )

        agente_riscos = AgenteRiscoPrazos()
        analise_riscos_prazos = agente_riscos.processar_contrato(
            texto_contrato=texto_completo,
            nome_arquivo=file_name
        )

        insights_proativos = gerar_insights_proativos(texto_contrato=texto_completo)

        return {
            "analise_automatica": analise_riscos_prazos,
            "insights_proativos_ia": insights_proativos
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        # Adicionando um print aqui também para vermos o erro exato no terminal
        print(f"--- ERRO 500 DETALHADO: {str(e)} ---")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado durante a análise: {str(e)}")