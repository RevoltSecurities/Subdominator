from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class PugreconResource(BaseResource):
    name = "pugrecon"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        json_body = {"domain_name": target}

        try:
            data = await self.client.request_json(
                "POST",
                "https://pugrecon.com/api/v1/domains",
                headers=headers,
                json_body=json_body,
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        if isinstance(data, dict):
            results = data.get("results", [])
            if isinstance(results, list):
                for item in results:
                    if isinstance(item, dict):
                        name = item.get("name")
                        if isinstance(name, str) and name:
                            findings.add(name)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
