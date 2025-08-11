"""
Exemplo de integração dos routers na aplicação FastAPI principal

Este arquivo demonstra como integrar todos os routers criados
em uma aplicação FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando os routers
from . import routers

def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI
    """
    app = FastAPI(
        title="AuditIA API",
        description="API para sistema de auditoria inteligente",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configuração de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, especificar domínios específicos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Incluindo todos os routers
    for router in routers:
        app.include_router(router)
    
    return app

# Exemplo de uso:
# app = create_app()

# Para executar:
# uvicorn app.main:app --reload

"""
Estrutura do arquivo main.py:

from fastapi import FastAPI
from app.routers.integration_example import create_app
from app.models.database import create_tables

# Criar tabelas na inicialização
create_tables()

# Criar aplicação
app = create_app()

@app.get("/")
def root():
    return {"message": "AuditIA API - Sistema de Auditoria Inteligente"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

"""
Exemplo de configuração com variáveis de ambiente:

import os
from fastapi import FastAPI
from app.routers.integration_example import create_app
from app.models.database import create_tables

# Configurações
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./audit_ia.db")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Criar tabelas
create_tables()

# Criar aplicação
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=HOST, 
        port=PORT,
        reload=DEBUG
    )
"""

"""
Exemplo de configuração com middleware adicional:

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app_with_middleware() -> FastAPI:
    app = FastAPI(
        title="AuditIA API",
        description="API para sistema de auditoria inteligente",
        version="1.0.0"
    )
    
    # Middleware de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Middleware de hosts confiáveis
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Em produção, especificar hosts
    )
    
    # Middleware de logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Tempo: {process_time:.4f}s"
        )
        
        return response
    
    # Incluindo routers
    from . import routers
    for router in routers:
        app.include_router(router)
    
    return app
"""

"""
Exemplo de configuração com autenticação:

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routers.integration_example import create_app

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implementar verificação de token JWT
    token = credentials.credentials
    # Verificar token...
    return token

def create_app_with_auth() -> FastAPI:
    app = create_app()
    
    # Adicionar dependência de autenticação aos routers
    # (implementar conforme necessário)
    
    return app
"""

"""
Exemplo de configuração com cache:

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis

def create_app_with_cache() -> FastAPI:
    app = create_app()
    
    # Configurar cache Redis
    redis_client = redis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis_client), prefix="auditia-cache")
    
    return app

# Exemplo de uso do cache em um endpoint:
# @cache(expire=60)
# async def get_cached_data():
#     return {"data": "cached"}
"""

"""
Exemplo de configuração com monitoramento:

from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram
import time

# Métricas Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

def create_app_with_monitoring() -> FastAPI:
    app = create_app()
    
    @app.middleware("http")
    async def monitor_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path
        ).inc()
        
        REQUEST_LATENCY.observe(process_time)
        
        return response
    
    return app
""" 