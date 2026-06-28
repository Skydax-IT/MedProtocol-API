from __future__ import annotations

from app.infrastructure.rules.loader import RuleCatalog, load_demo_catalog


class CapabilityService:
    def __init__(self, catalog: RuleCatalog | None = None) -> None:
        self.catalog = catalog or load_demo_catalog()

    def get_capabilities(self) -> dict[str, list[str] | str]:
        countries = sorted(self.catalog.country_packs)
        modules = sorted(
            {
                module
                for country in self.catalog.country_packs.values()
                for module in country.enabled_modules
            }
        )
        roles = sorted(self.catalog.scopes)
        languages = sorted(
            {
                language
                for country in self.catalog.country_packs.values()
                for language in country.languages
            }
        )
        return {
            "countries": countries,
            "modules": modules,
            "roles": roles,
            "languages": languages,
            "output_formats": ["json", "sms", "ussd"],
            "clinical_use_status": "not_for_real_patient_care",
        }
