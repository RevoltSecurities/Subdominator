from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class MySslResource(BaseResource):
    name = "myssl"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            data = await self.client.get_json(
                "https://myssl.com/api/v1/discover_sub_domain",
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [
            entry.get("domain", "")
            for entry in data.get("data", [])
            if isinstance(entry, dict)
            # Legacy filters: only subdomains that end with the target domain.
            and entry.get("domain", "").endswith(f".{target}")
        ]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
