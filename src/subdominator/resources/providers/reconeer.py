from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ReconeerResource(BaseResource):
    name = "reconeer"
    has_optional_config = True
    requires_config = False  # Matches OptionalKey requirement

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        headers = {
            "Accept": "application/json",
        }
        
        # Optional Key injection
        if self.provider_config:
            keys = self.provider_config.get_values(self.name)
            if keys and isinstance(keys, list):
                headers["X-API-KEY"] = str(keys[0])

        try:
            data = await self.client.get_json(
                f"https://www.reconeer.com/api/domain/{target}",
                headers=headers,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        if isinstance(data, dict):
            subdomains = data.get("subdomains", [])
            if isinstance(subdomains, list):
                for item in subdomains:
                    if isinstance(item, dict):
                        subds = item.get("subdomain")
                        if isinstance(subds, str) and subds:
                            findings.add(subds)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
