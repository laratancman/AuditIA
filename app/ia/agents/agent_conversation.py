from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_postgres.vectorstores import PGVector
from typing import Union

# <<< CORREÇÃO: Importa o LLM definido no seu arquivo models.py
from ..models import llm_gemini_flash 

# <<< CORREÇÃO: A lógica foi encapsulada em uma função que recebe os parâmetros necessários
def generate_embedding_response(db_retriever: PGVector, query: str, history: str) -> Union[dict, None]:
    """
    Busca documentos relevantes no banco de vetores e gera uma resposta conversacional.
    """
    template = """
                Você é um assistente cordial e especializado em contratos.

                Sua tarefa é usar:
                - Um parágrafo de contexto ({context}) com informações relevantes sobre contratos.
                - A pergunta feita pelo usuário ({input})
                - O histórico da conversa anterior ({history})

                Instruções:
                1. Leia com atenção o contexto ({context}) e identifique as informações mais úteis sobre os contratos.
                2. Verifique o histórico ({history}) para encontrar algo que complemente a resposta.
                3. Elabore uma resposta clara, objetiva e educada. Seja direto e vá ao ponto, sem rodeios desnecessários.
                4. **Só cumprimente o usuário (ex: “Olá”, “Oi”, “Bom dia”) se ele iniciar a pergunta com esse tipo de saudação.** Caso contrário, não cumprimente — apenas responda de forma direta e respeitosa.
                5. Se não for possível responder com as informações disponíveis, diga isso de forma educada, explicando que os dados não estão disponíveis ou que precisa de mais detalhes.

                Atenção:
                - Use apenas o conteúdo do contexto e histórico.
                - Não invente informações.
                - Nunca utilize conhecimento externo.

                Agora, responda à pergunta com base apenas no que foi fornecido.
            """
    try:
        prompt = PromptTemplate.from_template(template)

        # <<< CORREÇÃO: Usa a instância do LLM importada de models.py
        combine_docs_chain = create_stuff_documents_chain(llm_gemini_flash, prompt)
        
        # <<< CORREÇÃO: Cria o retriever a partir do banco de dados (db) passado como parâmetro
        retriever = db_retriever.as_retriever(
            search_kwargs={"k": 10}
        )
        
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        # <<< CORREÇÃO: Invoca a cadeia com os parâmetros corretos
        response = retrieval_chain.invoke({
            "input": query, 
            "history": history
        })
        
        return response
    except Exception as e:
        print(f"ERRO ao executar a cadeia de conversação: {e}")
        return None