from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ChinazResource(BaseResource):
    name = "chinaz"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                f"https://apidatav2.chinaz.com/single/alexa?key={key}&domain={target}",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: list[str] = []
        result = data.get("Result")
        
        if isinstance(result, dict):
            subdomain_list = result.get("ContributingSubdomainList", [])
            if isinstance(subdomain_list, list):
                for item in subdomain_list:
                    if isinstance(item, dict) and item.get("DataUrl"):
                        findings.append(item.get("DataUrl"))

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
