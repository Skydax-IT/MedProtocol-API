from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_authenticated_tenant, get_db
from app.application.services.next_question_service import NextQuestionService
from app.application.services.triage_service import TriageEvaluationService
from app.infrastructure.repositories.api_key_repository import AuthenticatedTenant
from app.schemas.triage import (
    NextQuestionRequest,
    NextQuestionResponse,
    TriageEvaluateRequest,
    TriageEvaluateResponse,
)

router = APIRouter(prefix="/triage", tags=["triage"])


@router.post("/evaluate", response_model=TriageEvaluateResponse)
def evaluate_triage(
    payload: TriageEvaluateRequest,
    request: Request,
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
    db: Annotated[Session, Depends(get_db)],
) -> TriageEvaluateResponse:
    return TriageEvaluationService(
        session=db,
        tenant=tenant,
        request_id=request.state.request_id,
    ).evaluate(payload)


@router.post("/next-question", response_model=NextQuestionResponse)
def next_question(
    payload: NextQuestionRequest,
    request: Request,
    tenant: Annotated[AuthenticatedTenant, Depends(get_authenticated_tenant)],
) -> NextQuestionResponse:
    return NextQuestionService(
        tenant=tenant,
        request_id=request.state.request_id,
    ).next_question(payload)
