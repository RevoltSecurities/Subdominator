from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class CyfareResource(BaseResource):
    name = "cyfare"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            data = await self.client.request_json(
                "POST",
                "https://cyfare.net/apps/VulnerabilityStudio/subfind/query.php",
                headers={"Origin": "https://cyfare.net", "Content-Type": "application/json"},
                json_body={"domain": target},
                expected_status={200},
            )
        except Exception:
            # Trap both RuntimeError (non-200) and JSONDecodeError (200 but bad layout payload)
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = data.get("subdomains", [])
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
