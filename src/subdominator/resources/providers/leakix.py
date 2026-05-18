from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class LeakIXResource(BaseResource):
    name = "leakix"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                f"https://leakix.net/api/subdomains/{target}",
                headers={"accept": "application/json", "api-key": key},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [entry.get("subdomain", "") for entry in data if isinstance(entry, dict)]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
