# Endpoints da API AuditIA

Este diretório contém todos os endpoints CRUD da API AuditIA, organizados por modelo de dados.

## Estrutura dos Endpoints

### 1. Users (`users.py`)
**Prefix:** `/users`
- **POST** `/` - Criar usuário
- **GET** `/` - Listar usuários (com filtros)
- **GET** `/{user_id}` - Obter usuário específico
- **PUT** `/{user_id}` - Atualizar usuário
- **DELETE** `/{user_id}` - Deletar usuário (soft delete)
- **PATCH** `/{user_id}/activate` - Reativar usuário
- **GET** `/{user_id}/documents` - Obter documentos do usuário

### 2. Documents (`documents.py`)
**Prefix:** `/documents`
- **POST** `/` - Criar documento (com upload de arquivo)
- **GET** `/` - Listar documentos (com filtros)
- **GET** `/{document_id}` - Obter documento específico
- **PUT** `/{document_id}` - Atualizar documento
- **DELETE** `/{document_id}` - Deletar documento
- **PATCH** `/{document_id}/status` - Atualizar status do documento
- **GET** `/{document_id}/clauses` - Obter cláusulas do documento
- **GET** `/{document_id}/entities` - Obter entidades do documento
- **GET** `/{document_id}/compliance-flags` - Obter flags de compliance
- **GET** `/{document_id}/deadline-alerts` - Obter alertas de prazo

### 3. Clauses (`clauses.py`)
**Prefix:** `/clauses`
- **POST** `/` - Criar cláusula
- **GET** `/` - Listar cláusulas (com filtros)
- **GET** `/{clause_id}` - Obter cláusula específica
- **PUT** `/{clause_id}` - Atualizar cláusula
- **DELETE** `/{clause_id}` - Deletar cláusula
- **PATCH** `/{clause_id}/status` - Atualizar status da cláusula
- **GET** `/{clause_id}/entities` - Obter entidades da cláusula
- **GET** `/{clause_id}/compliance-flags` - Obter flags de compliance
- **GET** `/types/` - Obter tipos de cláusulas
- **GET** `/categories/` - Obter categorias de cláusulas
- **GET** `/statistics/` - Obter estatísticas das cláusulas

### 4. Entities (`entities.py`)
**Prefix:** `/entities`
- **POST** `/` - Criar entidade
- **GET** `/` - Listar entidades (com filtros)
- **GET** `/{entity_id}` - Obter entidade específica
- **PUT** `/{entity_id}` - Atualizar entidade
- **DELETE** `/{entity_id}` - Deletar entidade
- **PATCH** `/{entity_id}/status` - Atualizar status da entidade
- **GET** `/types/` - Obter tipos de entidades
- **GET** `/categories/` - Obter categorias de entidades
- **GET** `/statistics/` - Obter estatísticas das entidades
- **GET** `/search/` - Buscar entidades por texto

### 5. Compliance Flags (`compliance_flags.py`)
**Prefix:** `/compliance-flags`
- **POST** `/` - Criar flag de compliance
- **GET** `/` - Listar flags (com filtros)
- **GET** `/{flag_id}` - Obter flag específica
- **PUT** `/{flag_id}` - Atualizar flag
- **DELETE** `/{flag_id}` - Deletar flag
- **PATCH** `/{flag_id}/status` - Atualizar status da flag
- **GET** `/types/` - Obter tipos de problemas
- **GET** `/categories/` - Obter categorias de flags
- **GET** `/statistics/` - Obter estatísticas das flags
- **GET** `/urgent/` - Obter flags urgentes
- **GET** `/expiring/` - Obter flags com prazo expirando

### 6. Deadline Alerts (`deadline_alerts.py`)
**Prefix:** `/deadline-alerts`
- **POST** `/` - Criar alerta de prazo
- **GET** `/` - Listar alertas (com filtros)
- **GET** `/{alert_id}` - Obter alerta específico
- **PUT** `/{alert_id}` - Atualizar alerta
- **DELETE** `/{alert_id}` - Deletar alerta
- **PATCH** `/{alert_id}/status` - Atualizar status do alerta
- **PATCH** `/{alert_id}/notify` - Marcar como notificado
- **GET** `/types/` - Obter tipos de prazos
- **GET** `/categories/` - Obter categorias de alertas
- **GET** `/statistics/` - Obter estatísticas dos alertas
- **GET** `/expiring/` - Obter alertas vencendo
- **GET** `/overdue/` - Obter alertas vencidos
- **GET** `/urgent/` - Obter alertas urgentes
- **GET** `/unnotified/` - Obter alertas não notificados

### 7. Reports (`reports.py`)
**Prefix:** `/reports`
- **POST** `/` - Criar relatório
- **GET** `/` - Listar relatórios (com filtros)
- **GET** `/{report_id}` - Obter relatório específico
- **PUT** `/{report_id}` - Atualizar relatório
- **DELETE** `/{report_id}` - Deletar relatório
- **PATCH** `/{report_id}/status` - Atualizar status do relatório
- **GET** `/types/` - Obter tipos de relatórios
- **GET** `/categories/` - Obter categorias de relatórios
- **GET** `/formats/` - Obter formatos de relatórios
- **GET** `/statistics/` - Obter estatísticas dos relatórios
- **GET** `/public/` - Obter relatórios públicos
- **GET** `/recent/` - Obter relatórios recentes
- **GET** `/by-user/{user_id}` - Obter relatórios por usuário

### 8. Feedbacks (`feedbacks.py`)
**Prefix:** `/feedbacks`
- **POST** `/` - Criar feedback
- **GET** `/` - Listar feedbacks (com filtros)
- **GET** `/{feedback_id}` - Obter feedback específico
- **PUT** `/{feedback_id}` - Atualizar feedback
- **DELETE** `/{feedback_id}` - Deletar feedback
- **PATCH** `/{feedback_id}/status` - Atualizar status do feedback
- **PATCH** `/{feedback_id}/respond` - Responder ao feedback
- **GET** `/types/` - Obter tipos de feedback
- **GET** `/categories/` - Obter categorias de feedback
- **GET** `/statistics/` - Obter estatísticas dos feedbacks
- **GET** `/open/` - Obter feedbacks abertos
- **GET** `/high-priority/` - Obter feedbacks de alta prioridade
- **GET** `/anonymous/` - Obter feedbacks anônimos
- **GET** `/by-user/{user_id}` - Obter feedbacks por usuário

## Características dos Endpoints

### Validação de Dados
- Todos os endpoints usam schemas Pydantic para validação
- Validação automática de tipos de dados
- Validação de relacionamentos entre entidades

### Tratamento de Erros
- **404 Not Found**: Recurso não encontrado
- **400 Bad Request**: Dados inválidos ou conflitos
- **422 Unprocessable Entity**: Erro de validação do Pydantic

### Filtros e Paginação
- Parâmetros de query para filtros opcionais
- Paginação com `skip` e `limit`
- Ordenação por campos específicos

### Relacionamentos
- Endpoints para acessar dados relacionados
- Validação de integridade referencial
- Soft delete onde apropriado

### Estatísticas e Relatórios
- Endpoints específicos para estatísticas
- Agregações por diferentes critérios
- Métricas de performance e uso

## Exemplo de Uso

```python
# Criar um usuário
POST /users/
{
    "nome": "João Silva",
    "email": "joao@empresa.com",
    "senha": "senha123",
    "permissao": "auditor"
}

# Upload de documento
POST /documents/
FormData:
- file: contrato.pdf
- titulo: "Contrato de Fornecimento"
- tipo_documento: "contrato"
- user_id: 1

# Listar cláusulas de um documento
GET /documents/1/clauses

# Criar flag de compliance
POST /compliance-flags/
{
    "tipo_problema": "prazo_curto",
    "categoria": "temporal",
    "descricao": "Prazo muito curto identificado",
    "document_id": 1,
    "severidade": "alta"
}
```

## Próximos Passos

1. **Autenticação e Autorização**
   - Implementar JWT tokens
   - Controle de acesso baseado em roles
   - Middleware de autenticação

2. **Validações de Negócio**
   - Regras específicas do domínio
   - Validações complexas entre entidades
   - Workflows de aprovação

3. **Performance**
   - Índices de banco de dados
   - Cache de consultas frequentes
   - Paginação otimizada

4. **Logs e Monitoramento**
   - Logs de auditoria
   - Métricas de performance
   - Alertas de erro

5. **Testes**
   - Testes unitários
   - Testes de integração
   - Testes de performance 