from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DigitalYamaResource(BaseResource):
    name = "digitalyama"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://api.digitalyama.com/subdomain_finder",
                headers={"x-api-key": key},
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = data.get("subdomains", [])
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
