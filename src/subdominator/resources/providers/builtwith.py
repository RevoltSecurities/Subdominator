from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class BuiltWithResource(BaseResource):
    name = "builtwith"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://api.builtwith.com/v21/api.json",
                params={
                    "KEY": key,
                    "HIDETEXT": "yes",
                    "HIDEDL": "yes",
                    "NOLIVE": "yes",
                    "NOMETA": "yes",
                    "NOPII": "yes",
                    "NOATTR": "yes",
                    "LOOKUP": target,
                },
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: list[str] = []
        for result in data.get("Results", []):
            for chunk in result.get("Result", {}).get("Paths", []):
                domain_name = chunk.get("Domain", "")
                subdomain = chunk.get("SubDomain", "")
                if domain_name and subdomain:
                    findings.append(f"{subdomain}.{domain_name}")
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
