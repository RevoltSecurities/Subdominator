from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class CodeRogResource(BaseResource):
    name = "coderog"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://subdomain-finder5.p.rapidapi.com/subdomain-finder",
                headers={
                    "x-rapidapi-key": key,
                    "x-rapidapi-host": "subdomain-finder5.p.rapidapi.com",
                },
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [item.get("subdomain", "") for item in data.get("data", []) if isinstance(item, dict)]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
