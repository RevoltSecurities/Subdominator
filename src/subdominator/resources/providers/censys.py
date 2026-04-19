from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class CensysResource(BaseResource):
    name = "censys"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        api_id, api_secret = self.get_required_pair()
        if api_id is None or api_secret is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        cursor: str | None = None
        findings: set[str] = set()

        for _ in range(11):
            params: dict[str, str] = {"q": target, "per_page": "100"}
            if cursor:
                params["cursor"] = cursor

            try:
                data = await self.client.get_json(
                    "https://search.censys.io/api/v2/certificates/search",
                    headers={"Authorization": self.client.basic_auth_header(api_id, api_secret)},
                    params=params,
                    expected_status={200},
                )
            except RuntimeError:
                break

            result = data.get("result", {})
            hits = result.get("hits", [])
            if not hits:
                break

            for hit in hits:
                findings.update(str(name) for name in hit.get("names", []))

            cursor = result.get("links", {}).get("next")
            if not cursor:
                break

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
