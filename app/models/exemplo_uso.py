"""
Exemplo de uso dos modelos do sistema AuditIA

Este arquivo demonstra como usar os modelos SQLAlchemy e schemas Pydantic
em uma aplicação FastAPI.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

# Importando os modelos
from . import (
    User, Document, Clause, Entity, ComplianceFlag, 
    DeadlineAlert, Report, Feedback,
    UserCreate, DocumentCreate, ClauseCreate, EntityCreate,
    ComplianceFlagCreate, DeadlineAlertCreate, ReportCreate, FeedbackCreate
)
from .database import get_db

# Exemplo de criação de usuário
def criar_usuario_exemplo(db: Session):
    """Exemplo de criação de um usuário"""
    user_data = UserCreate(
        nome="João Silva",
        email="joao.silva@empresa.com",
        permissao="auditor",
        telefone="(11) 99999-9999",
        departamento="Compliance",
        cargo="Auditor Senior"
    )
    
    # Em uma aplicação real, você hasharia a senha
    user = User(
        **user_data.dict(),
        senha_hash="senha_hash_aqui"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Exemplo de criação de documento
def criar_documento_exemplo(db: Session, user_id: int):
    """Exemplo de criação de um documento"""
    document_data = DocumentCreate(
        titulo="Contrato de Fornecimento 2024",
        descricao="Contrato anual de fornecimento de materiais",
        tipo_documento="contrato",
        numero_contrato="CONTR-2024-001",
        valor_contrato="R$ 500.000,00",
        data_vencimento=datetime.now() + timedelta(days=365),
        nome_arquivo="contrato_fornecimento_2024.pdf",
        tipo_arquivo="pdf",
        tamanho_arquivo=1024000
    )
    
    document = Document(
        **document_data.dict(),
        user_id=user_id,
        caminho_arquivo="/uploads/contrato_fornecimento_2024.pdf",
        status="pendente"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

# Exemplo de criação de cláusula
def criar_clausula_exemplo(db: Session, document_id: int):
    """Exemplo de criação de uma cláusula detectada"""
    clause_data = ClauseCreate(
        texto="O fornecedor deverá entregar os produtos no prazo máximo de 30 dias",
        tipo_clausula="prazo_entrega",
        categoria="temporal",
        posicao_inicio=150,
        posicao_fim=200,
        pagina=3,
        confianca=0.95,
        relevancia="alta",
        contexto="Cláusula 5.2 - Prazo de Entrega"
    )
    
    clause = Clause(
        **clause_data.dict(),
        document_id=document_id
    )
    
    db.add(clause)
    db.commit()
    db.refresh(clause)
    return clause

# Exemplo de criação de entidade
def criar_entidade_exemplo(db: Session, document_id: int, clause_id: int = None):
    """Exemplo de criação de uma entidade extraída"""
    entity_data = EntityCreate(
        texto="30 dias",
        tipo_entidade="prazo",
        categoria="temporal",
        valor_normalizado="P30D",
        posicao_inicio=180,
        posicao_fim=188,
        pagina=3,
        confianca=0.92,
        relevancia="alta",
        contexto="prazo máximo de 30 dias",
        clause_id=clause_id
    )
    
    entity = Entity(
        **entity_data.dict(),
        document_id=document_id
    )
    
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity

# Exemplo de criação de flag de compliance
def criar_compliance_flag_exemplo(db: Session, document_id: int, clause_id: int = None):
    """Exemplo de criação de uma flag de compliance"""
    flag_data = ComplianceFlagCreate(
        tipo_problema="prazo_curto",
        categoria="temporal",
        severidade="media",
        descricao="Prazo de entrega de 30 dias pode ser insuficiente para grandes volumes",
        recomendacao="Considerar prorrogação do prazo ou divisão em lotes menores",
        prioridade="media",
        data_limite=datetime.now() + timedelta(days=7),
        responsavel="Departamento de Compras",
        acao_requerida="Revisar prazo com fornecedor",
        impacto="medio",
        risco="medio",
        clause_id=clause_id
    )
    
    flag = ComplianceFlag(
        **flag_data.dict(),
        document_id=document_id
    )
    
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return flag

# Exemplo de criação de alerta de prazo
def criar_deadline_alert_exemplo(db: Session, document_id: int):
    """Exemplo de criação de um alerta de prazo"""
    alert_data = DeadlineAlertCreate(
        titulo="Vencimento do Contrato de Fornecimento",
        descricao="Contrato vence em 30 dias",
        tipo_prazo="vencimento",
        categoria="temporal",
        data_limite=datetime.now() + timedelta(days=30),
        data_lembrete=datetime.now() + timedelta(days=15),
        prioridade="alta",
        severidade="alta",
        dias_antecedencia=30,
        acao_requerida="Renovar ou encerrar contrato",
        responsavel="Gerente de Compras"
    )
    
    alert = DeadlineAlert(
        **alert_data.dict(),
        document_id=document_id
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

# Exemplo de criação de relatório
def criar_relatorio_exemplo(db: Session, user_id: int, document_id: int):
    """Exemplo de criação de um relatório"""
    report_data = ReportCreate(
        titulo="Relatório de Compliance - Contrato 2024",
        descricao="Análise completa de compliance do contrato",
        tipo_relatorio="compliance",
        categoria="legal",
        formato="pdf",
        resumo_executivo="Contrato apresenta 3 pontos de atenção que requerem ação",
        principais_achados="Prazos curtos, valores elevados e cláusulas de penalidade inadequadas",
        recomendacoes="Revisar prazos, negociar valores e ajustar penalidades",
        prioridade="alta",
        parametros={"periodo": "2024", "tipo_analise": "completa"},
        document_id=document_id
    )
    
    report = Report(
        **report_data.dict(),
        user_id=user_id,
        caminho_arquivo="/reports/relatorio_compliance_2024.pdf",
        tamanho_arquivo=2048000
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

# Exemplo de criação de feedback
def criar_feedback_exemplo(db: Session, user_id: int, document_id: int):
    """Exemplo de criação de um feedback"""
    feedback_data = FeedbackCreate(
        tipo_feedback="sugestao",
        categoria="interface",
        titulo="Melhorar visualização de cláusulas",
        descricao="Seria útil ter uma visualização mais clara das cláusulas detectadas",
        avaliacao=4,
        satisfacao=0.8,
        prioridade="media",
        impacto="medio",
        document_id=document_id
    )
    
    feedback = Feedback(
        **feedback_data.dict(),
        user_id=user_id
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

# Exemplo de consultas
def consultar_documentos_por_usuario(db: Session, user_id: int) -> List[Document]:
    """Exemplo de consulta de documentos por usuário"""
    return db.query(Document).filter(Document.user_id == user_id).all()

def consultar_clausulas_por_documento(db: Session, document_id: int) -> List[Clause]:
    """Exemplo de consulta de cláusulas por documento"""
    return db.query(Clause).filter(Clause.document_id == document_id).all()

def consultar_flags_abertas(db: Session) -> List[ComplianceFlag]:
    """Exemplo de consulta de flags de compliance abertas"""
    return db.query(ComplianceFlag).filter(ComplianceFlag.status == "aberto").all()

def consultar_alertas_vencendo(db: Session, dias: int = 30) -> List[DeadlineAlert]:
    """Exemplo de consulta de alertas vencendo em X dias"""
    data_limite = datetime.now() + timedelta(days=dias)
    return db.query(DeadlineAlert).filter(
        DeadlineAlert.data_limite <= data_limite,
        DeadlineAlert.status == "ativo"
    ).all()

# Exemplo de uso completo
def exemplo_completo():
    """Exemplo completo de uso dos modelos"""
    # Em uma aplicação FastAPI, você usaria get_db() como dependency
    # Aqui é apenas um exemplo
    print("Exemplo de uso dos modelos AuditIA")
    print("=" * 50)
    
    # Este seria usado em um endpoint FastAPI
    # db = next(get_db())
    
    print("Modelos criados com sucesso!")
    print("- User: Gerenciamento de usuários")
    print("- Document: Documentos e contratos")
    print("- Clause: Cláusulas detectadas")
    print("- Entity: Entidades extraídas")
    print("- ComplianceFlag: Alertas de compliance")
    print("- DeadlineAlert: Alertas de prazos")
    print("- Report: Relatórios gerados")
    print("- Feedback: Feedbacks de usuários")
    
    print("\nPara usar em FastAPI:")
    print("1. Importe os modelos: from app.models import User, Document, etc.")
    print("2. Use get_db como dependency: def endpoint(db: Session = Depends(get_db))")
    print("3. Use os schemas Pydantic para validação de dados")
    print("4. Use os modelos SQLAlchemy para operações no banco")

if __name__ == "__main__":
    exemplo_completo() 