from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RapidScanResource(BaseResource):
    name = "rapidscan"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://subdomain-scan1.p.rapidapi.com/",
                headers={
                    "X-RapidAPI-Key": key,
                    "X-RapidAPI-Host": "subdomain-scan1.p.rapidapi.com",
                },
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        # Guard: API should return a list; if it returns an error dict instead,
        # iterating over the dict keys would produce garbage strings.
        if not isinstance(data, list):
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [str(item) for item in data]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
