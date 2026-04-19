from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class BinaryEdgeResource(BaseResource):
    name = "binaryedge"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        page = 1
        page_size = 100
        findings: set[str] = set()

        while True:
            try:
                data = await self.client.get_json(
                    f"https://api.binaryedge.io/v2/query/domains/subdomain/{target}",
                    headers={"X-Key": key},
                    params={"page": str(page), "pagesize": str(page_size)},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 (rate-limit, quota, etc.) — return what we have.
                break

            events = data.get("events", [])
            if not events:
                break

            findings.update(str(event) for event in events)
            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
