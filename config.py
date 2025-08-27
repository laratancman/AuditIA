import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")


# REGRAS_RISCO é um dicionário que mapeia um TIPO de risco a uma lista de PALAVRAS-CHAVE.
# O agente irá procurar por essas palavras-chave no texto do contrato para gerar alertas.
#
# Como usar:
# - A CHAVE (ex: "RESCISAO") é o nome do risco que será retornado no alerta.
# - O VALOR (ex: ["rescisão", "rescindir"]) é a lista de termos que acionam esse alerta.
#
# Dicas para melhorar a detecção:
# - Use palavras em minúsculo e sem acentos para uma correspondência mais ampla.
# - Adicione variações da mesma palavra (ex: "rescindir", "rescisão", "rescindido").
# - Pense em sinônimos e termos relacionados ao risco.
# - Você pode adicionar quantas categorias e palavras-chave desejar.

REGRAS_RISCO = {
    "RESCISAO": [
        "rescisão", "rescindir", "cancelamento", "terminar o contrato",
        "extinção do contrato", "denunciar o contrato", "resolução contratual",
        "distrato"
    ],
    "MULTA": [
        "multa", "penalidade", "penalidades", "sanção", "sanções",
        "cláusula penal", "astreintes", "juros de mora", "correção monetária"
    ],
    "CONFIDENCIALIDADE": [
        "confidencial", "confidencialidade", "sigilo", "sigiloso",
        "não divulgar", "informação confidencial", "segredo comercial", "nda"
    ],
    "LGPD": [
        "lgpd", "lei geral de proteção de dados", "dados pessoais",
        "tratamento de dados", "controlador de dados", "operador de dados",
        "privacidade de dados"
    ],
    "PROPRIEDADE_INTELECTUAL": [
        "propriedade intelectual", "direitos autorais", "patente", "patentes",
        "marca registrada", "marcas", "copyright", "licenciamento de software"
    ],
    "OBRIGACAO_DE_PAGAMENTO": [
        "pagamento", "pagar", "remuneração", "preço", "honorários",
        "fatura", "cobrança", "reajuste de preço"
    ],
    "INDENIZACAO": [
        "indenização", "indenizar", "reparação", "danos", "perdas e danos",
        "responsabilidade civil", "ressarcir"
    ],
    "FORO_E_LEGISLACAO": [
        "foro", "jurisdição", "comarca", "lei aplicável", "legislação brasileira",
        "arbitragem"
    ],
    "GARANTIA": [
        "garantia", "garante", "assegura", "livre de defeitos", "período de garantia"
    ]
}
