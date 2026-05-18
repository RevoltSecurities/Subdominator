from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RapidFinderResource(BaseResource):
    name = "rapidfinder"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://subdomain-finder3.p.rapidapi.com/v1/subdomain-finder/",
                headers={
                    "X-RapidAPI-Key": key,
                    "X-RapidAPI-Host": "subdomain-finder3.p.rapidapi.com",
                },
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [item.get("subdomain", "") for item in data.get("subdomains", []) if isinstance(item, dict)]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
