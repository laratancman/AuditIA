# Modelos do Sistema AuditIA

Este diretório contém todos os modelos de dados do sistema AuditIA, implementados usando SQLAlchemy para o banco de dados e Pydantic para validação de dados na API.

## Estrutura dos Modelos

### 1. User (Usuário)
**Arquivo:** `user.py`
- **Propósito:** Gerenciar informações dos usuários do sistema
- **Campos principais:**
  - `nome`: Nome completo do usuário
  - `email`: Email único do usuário
  - `senha_hash`: Hash da senha (não armazenar senha em texto plano)
  - `permissao`: Nível de acesso (admin, auditor, usuario)
  - `ativo`: Status do usuário
  - `departamento`, `cargo`: Informações organizacionais

### 2. Document (Documento)
**Arquivo:** `document.py`
- **Propósito:** Representar contratos e arquivos enviados
- **Campos principais:**
  - `titulo`: Título do documento
  - `nome_arquivo`, `caminho_arquivo`: Informações do arquivo
  - `tipo_arquivo`: Formato (pdf, docx, etc.)
  - `status`: Status do processamento (pendente, processando, analisado, erro)
  - `tipo_documento`: Tipo (contrato, aditivo, anexo, etc.)
  - `numero_contrato`, `valor_contrato`: Informações específicas de contratos

### 3. Clause (Cláusula)
**Arquivo:** `clause.py`
- **Propósito:** Armazenar cláusulas detectadas em documentos
- **Campos principais:**
  - `texto`: Texto da cláusula
  - `tipo_clausula`: Tipo (penalidade, prazo, valor, etc.)
  - `categoria`: Categoria (financeira, temporal, responsabilidade, etc.)
  - `posicao_inicio`, `posicao_fim`: Posição no documento
  - `confianca`: Score de confiança da detecção (0-1)
  - `relevancia`: Nível de relevância (baixa, media, alta, critica)

### 4. Entity (Entidade)
**Arquivo:** `entity.py`
- **Propósito:** Guardar entidades identificadas por PLN
- **Campos principais:**
  - `texto`: Texto da entidade
  - `tipo_entidade`: Tipo (data, valor, pessoa, empresa, etc.)
  - `valor_normalizado`: Valor padronizado
  - `confianca`: Score de confiança
  - `contexto`: Texto ao redor da entidade

### 5. ComplianceFlag (Sinalização de Compliance)
**Arquivo:** `compliance_flag.py`
- **Propósito:** Armazenar alertas de não conformidade
- **Campos principais:**
  - `tipo_problema`: Tipo do problema identificado
  - `categoria`: Categoria (financeira, temporal, legal, etc.)
  - `severidade`: Nível de severidade (baixa, media, alta, critica)
  - `descricao`: Descrição do problema
  - `recomendacao`: Recomendação de ação
  - `status`: Status (aberto, em_analise, resolvido, ignorado)

### 6. DeadlineAlert (Alerta de Prazo)
**Arquivo:** `deadline_alert.py`
- **Propósito:** Controlar prazos relevantes dos contratos
- **Campos principais:**
  - `titulo`: Título do alerta
  - `tipo_prazo`: Tipo (vencimento, renovacao, pagamento, etc.)
  - `data_limite`: Data limite do prazo
  - `data_lembrete`: Data para lembrar
  - `status`: Status (ativo, vencido, renovado, cancelado)
  - `dias_antecedencia`: Dias antes do prazo para alertar

### 7. Report (Relatório)
**Arquivo:** `report.py`
- **Propósito:** Estrutura para relatórios gerados pelo sistema
- **Campos principais:**
  - `titulo`: Título do relatório
  - `tipo_relatorio`: Tipo (compliance, analise, resumo, etc.)
  - `formato`: Formato (pdf, docx, html, json)
  - `resumo_executivo`: Resumo executivo
  - `principais_achados`: Principais achados
  - `recomendacoes`: Recomendações

### 8. Feedback (Feedback)
**Arquivo:** `feedback.py`
- **Propósito:** Guardar feedbacks de usuários (opcional)
- **Campos principais:**
  - `tipo_feedback`: Tipo (analise, sugestao, erro, melhoria)
  - `titulo`, `descricao`: Informações do feedback
  - `avaliacao`: Avaliação (1-5 estrelas)
  - `satisfacao`: Score de satisfação (0-1)
  - `status`: Status (aberto, em_analise, resolvido, rejeitado)

## Configuração da Base de Dados

### Arquivo: `database.py`
- **Configuração:** Centraliza a configuração do SQLAlchemy
- **Funções principais:**
  - `get_db()`: Dependency para FastAPI
  - `create_tables()`: Criar todas as tabelas
  - `drop_tables()`: Remover todas as tabelas (desenvolvimento)

## Relacionamentos

Os modelos possuem relacionamentos bem definidos:

```
User (1) ←→ (N) Document
Document (1) ←→ (N) Clause
Document (1) ←→ (N) Entity
Document (1) ←→ (N) ComplianceFlag
Document (1) ←→ (N) DeadlineAlert
Document (1) ←→ (N) Report
Document (1) ←→ (N) Feedback

Clause (1) ←→ (N) Entity
Clause (1) ←→ (N) ComplianceFlag
Clause (1) ←→ (N) Feedback

Entity (1) ←→ (N) Feedback

User (1) ←→ (N) ComplianceFlag
User (1) ←→ (N) DeadlineAlert
User (1) ←→ (N) Report
User (1) ←→ (N) Feedback
```

## Schemas Pydantic

Cada modelo possui schemas Pydantic para validação de dados:

- **Base**: Schema base com campos comuns
- **Create**: Schema para criação (sem ID)
- **Update**: Schema para atualização (campos opcionais)
- **Response**: Schema para resposta da API

## Uso em FastAPI

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models import get_db, User, UserCreate

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Lógica para criar usuário
    pass
```

## Exemplo de Uso

Veja o arquivo `exemplo_uso.py` para exemplos completos de como usar os modelos.

## Configuração

1. **Variável de ambiente:** `DATABASE_URL` (padrão: SQLite)
2. **Criar tabelas:** `create_tables()` na inicialização
3. **Dependency:** Use `get_db()` nos endpoints FastAPI

## Próximos Passos

1. Implementar autenticação e autorização
2. Criar endpoints CRUD para cada modelo
3. Implementar validações de negócio
4. Adicionar índices para performance
5. Implementar soft delete onde apropriado 