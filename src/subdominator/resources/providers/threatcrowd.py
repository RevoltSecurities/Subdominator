from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ThreatCrowdResource(BaseResource):
    name = "threatcrowd"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        # Legacy used http://ci-www.threatcrowd.org/ — switch to HTTPS for the
        # public mirror that is still intermittently available. Bail on non-200
        # so timeouts and 5xx are recorded as resource errors, not crashes.
        try:
            data = await self.client.get_json(
                "https://ci-www.threatcrowd.org/searchApi/v2/domain/report/",
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [
            subdomain
            for subdomain in data.get("subdomains", [])
            if subdomain and subdomain.endswith(f".{target}")
        ]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
