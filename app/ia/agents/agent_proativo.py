from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from ..models import GEMINI_API_KEY
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold

def gerar_insights_proativos(texto_contrato: str) -> str:
    """
    Analisa o texto de um contrato e gera insights, riscos e dicas de forma proativa.
    """
    print("--- DEBUG: Entrou na função gerar_insights_proativos ---")

    # Instância do LLM com configurações de segurança personalizadas
    llm_proativo_seguro = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    # --- PROMPT NOVO E MELHORADO ---
    template = """
        Você é um consultor de contratos da AuditIA, um especialista em transformar documentos complexos em insights claros e acionáveis para executivos.

        **Objetivo:** Analisar o contrato fornecido e gerar um resumo executivo, elegante e conciso.

        **Formato da Resposta:**
        - Use Markdown para formatação (**negrito**, tópicos).
        - Inicie cada seção com um emoji correspondente para clareza visual.
        - Seja extremamente direto e focado no que é mais importante.

        **Estrutura Obrigatória:**

        📄 **Resumo do Contrato:**
        Em uma única frase, descreva o propósito principal deste documento.

        ⚠️ **Pontos de Atenção:**
        Liste no máximo 3 a 4 tópicos essenciais. Para cada tópico, explique o impacto em termos de negócio (risco, custo, obrigação) de forma breve.
        - **[Tópico 1]:** Breve explicação.
        - **[Tópico 2]:** Breve explicação.
        - **[Tópico 3]:** Breve explicação.

        💡 **Recomendação Estratégica:**
        Forneça uma única recomendação clara e acionável para o próximo passo.

        ---
        Texto do Contrato para Análise:
        {contrato}
        ---
    """
    
    try:
        prompt = PromptTemplate.from_template(template)
        
        # Use a instância do LLM com as configurações de segurança
        chain = prompt | llm_proativo_seguro
        
        print("--- DEBUG: Prestes a invocar a API do Gemini com o novo prompt... ---")
        response = chain.invoke({"contrato": texto_contrato})
        print("--- DEBUG: A API do Gemini respondeu com sucesso! ---")
        
        return response.content

    except Exception as e:
        print(f"--- ERRO CAPTURADO EM gerar_insights_proativos: {str(e)} ---")
        raise e