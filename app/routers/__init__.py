# Importando todos os routers
from .users import router as users_router
from .documents import router as documents_router
from .clauses import router as clauses_router
from .entities import router as entities_router
from .compliance_flags import router as compliance_flags_router
from .deadline_alerts import router as deadline_alerts_router
from .reports import router as reports_router
from .feedbacks import router as feedbacks_router

# Lista de todos os routers
routers = [
    users_router,
    documents_router,
    clauses_router,
    entities_router,
    compliance_flags_router,
    deadline_alerts_router,
    reports_router,
    feedbacks_router
]

__all__ = [
    "routers",
    "users_router",
    "documents_router", 
    "clauses_router",
    "entities_router",
    "compliance_flags_router",
    "deadline_alerts_router",
    "reports_router",
    "feedbacks_router"
]
