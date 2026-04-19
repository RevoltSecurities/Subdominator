from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DomScanResource(BaseResource):
    name = "domscan"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {"X-API-Key": key}
        findings: set[str] = set()

        try:
            data = await self.client.get_json(
                f"https://domscan.net/v1/subdomains?domain={target}",
                headers=headers,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        if isinstance(data, dict):
            subdomains = data.get("subdomains", [])
            if isinstance(subdomains, list):
                for item in subdomains:
                    if isinstance(item, str) and item:
                        findings.add(item)

        return ResourceResult(
            self.name, target, recursion_depth, self.normalize_findings(target, findings)
        )
