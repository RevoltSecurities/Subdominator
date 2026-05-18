from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RacentResource(BaseResource):
    name = "racent"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            data = await self.client.get_json(
                "https://face.racent.com/tool/query_ctlog",
                params={"keyword": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: list[str] = []
        for item in data.get("data", {}).get("list", []):
            findings.extend(item.get("dnsnames", []))
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
