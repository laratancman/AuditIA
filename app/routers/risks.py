import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

# Importa o seu agente e a função para ler PDF
from app.ia.agents.agent_risco_prazos import AgenteRiscoPrazos
from app.ia.utils import read_pdf # Supondo que você tenha essa função em utils.py

# Cria um novo router para este endpoint
router = APIRouter(prefix="/analysis", tags=["Análise de Riscos e Prazos"])

@router.post("/process-contract")
def process_contract_endpoint(file: UploadFile = File(...)):
    """
    Endpoint para receber um contrato em PDF, processá-lo com o 
    AgenteRiscoPrazos e retornar a análise completa.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF.")

    temp_path = None
    try:
        # --- ETAPA 1: Salvar o arquivo PDF temporariamente ---
        # É necessário salvar para que a biblioteca de leitura de PDF possa abri-lo
        tmp_dir = "/tmp/audit_ia_risks"
        os.makedirs(tmp_dir, exist_ok=True)
        temp_path = os.path.join(tmp_dir, f"{uuid.uuid4()}_{file.filename}")
        
        with open(temp_path, "wb") as f:
            f.write(file.file.read())

        # --- ETAPA 2: Extrair o texto do PDF ---
        # Usamos uma função auxiliar para converter o PDF em texto
        pdf_pages = read_pdf(file_path=temp_path)
        if not pdf_pages:
            raise HTTPException(status_code=400, detail="Não foi possível extrair texto do PDF.")
        
        # Concatena o texto de todas as páginas em uma única string
        texto_completo_contrato = "\n".join([page.page_content for page in pdf_pages])

        # --- ETAPA 3: Processar o texto com o Agente ---
        # Instancia o agente e chama o método de processamento
        agente = AgenteRiscoPrazos(dias_alerta_proximo=30)
        resultado_analise = agente.processar_contrato(
            texto_contrato=texto_completo_contrato,
            nome_arquivo=file.filename
        )

        # --- ETAPA 4: Retornar o resultado ---
        return resultado_analise

    except Exception as e:
        # Captura qualquer erro inesperado durante o processo
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado: {str(e)}")

    finally:
        # --- ETAPA 5: Limpeza ---
        # Garante que o arquivo temporário seja sempre excluído
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
