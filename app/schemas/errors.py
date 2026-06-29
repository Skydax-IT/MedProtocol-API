from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.common import StrictBaseModel


class ErrorDetail(StrictBaseModel):
    field: str | None = None
    issue: str


class ErrorBody(StrictBaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)


class ErrorMeta(StrictBaseModel):
    request_id: str


class ErrorResponse(StrictBaseModel):
    error: ErrorBody
    meta: ErrorMeta


def validation_details(errors: list[dict[str, Any]]) -> list[ErrorDetail]:
    details: list[ErrorDetail] = []
    for item in errors:
        loc = ".".join(str(part) for part in item.get("loc", []) if part != "body")
        details.append(ErrorDetail(field=loc or None, issue=str(item.get("msg", "Invalid input"))))
    return details
