from __future__ import annotations

from fastapi import APIRouter

from app.api import demo
from app.api.v1 import audit, capabilities, health, offline, protocols, triage, version

router = APIRouter()
router.include_router(health.router)
router.include_router(version.router)
router.include_router(demo.router)
router.include_router(capabilities.router, prefix="/v1")
router.include_router(protocols.router, prefix="/v1")
router.include_router(triage.router, prefix="/v1")
router.include_router(audit.router, prefix="/v1")
router.include_router(offline.router, prefix="/v1")
