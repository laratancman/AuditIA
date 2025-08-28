from langchain.prompts import PromptTemplate
from ..models import llm_gemini_pro

def gerar_insights_proativos(texto_contrato: str) -> str:
    """
    Analisa o texto de um contrato e gera insights, riscos e dicas de forma proativa.

    :param texto_contrato: O conteúdo textual completo do contrato.
    :return: Uma análise textual gerada pela IA.
    """

    template = """
        Você é um advogado especialista sênior, encarregado de revisar um contrato para um cliente. Sua tarefa é ler o texto a seguir e, de forma proativa, criar um resumo com os pontos mais importantes que o cliente precisa saber.

        Seu resumo deve ser claro, objetivo e em formato de tópicos (bullet points).

        Instruções:
        1.  **Resumo Executivo:** Comece com um parágrafo curto resumindo o propósito principal do contrato.
        2.  **Pontos de Atenção Críticos:** Identifique e liste as 3 a 5 cláusulas ou obrigações mais importantes que podem gerar riscos (multas, rescisão, confidencialidade, LGPD, propriedade intelectual). Explique o risco de forma simples.
        3.  **Prazos e Datas Importantes:** Se houver datas ou prazos mencionados, liste-os claramente.
        4.  **Dicas de Negociação (Opcional):** Se identificar alguma cláusula que parece desfavorável ou que poderia ser negociada, sugira uma alternativa ou um ponto para discussão.
        5.  **Linguagem:** Use uma linguagem de negócios, mas evite jargões legais excessivos para que o cliente possa entender.

        Aja como um consultor de confiança. Sua análise deve ser direta e útil.

        Abaixo está o texto do contrato:
        ---
        {contrato}
        ---

        Agora, forneça sua análise proativa.
    """

    try:
        prompt = PromptTemplate.from_template(template)

        chain = prompt | llm_gemini_pro

        response = chain.invoke({"contrato": texto_contrato})

        return response.content

    except Exception as e:
        print(f"ERRO ao gerar insights proativos: {e}")
        return "Não foi possível gerar os insights devido a um erro interno."