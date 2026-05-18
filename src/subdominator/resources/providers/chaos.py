from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ChaosResource(BaseResource):
    name = "chaos"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                f"https://dns.projectdiscovery.io/dns/{target}/subdomains",
                headers={"Authorization": key},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [f"{item}.{target}" for item in data.get("subdomains", [])]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
