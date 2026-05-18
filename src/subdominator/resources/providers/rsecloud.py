from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RseCloudResource(BaseResource):
    name = "rsecloud"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        page = 1
        total_pages = 1
        findings: set[str] = set()

        # Legacy pattern: fetch page 1 to learn total_pages, then continue
        # until page > total_pages or batch is empty.
        while page <= total_pages:
            try:
                data = await self.client.request_json(
                    "POST",
                    "https://api.rsecloud.com/api/v1/subdomains",
                    headers={"X-API-Key": key, "Content-Type": "application/json"},
                    params={"page": str(page)},
                    json_body={"domain": target},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 (rate-limit / auth failure) — return what we have.
                break

            if "error" in data:
                break

            batch = data.get("data", [])
            if not batch:
                break

            findings.update(str(item) for item in batch)
            total_pages = int(data.get("total_pages", total_pages))
            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
