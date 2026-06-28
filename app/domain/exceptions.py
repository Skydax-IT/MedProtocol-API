from __future__ import annotations


class DomainError(Exception):
    code = "DOMAIN_ERROR"


class RuleEvaluationError(DomainError):
    code = "RULE_ENGINE_ERROR"


class UnsupportedCountryError(DomainError):
    code = "COUNTRY_NOT_ENABLED"


class UnsupportedModuleError(DomainError):
    code = "MODULE_NOT_ENABLED"


class UnsupportedRoleError(DomainError):
    code = "FORBIDDEN"


class SafetyViolationError(DomainError):
    code = "RULE_ENGINE_ERROR"
