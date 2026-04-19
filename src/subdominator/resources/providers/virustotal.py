from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class VirusTotalResource(BaseResource):
    name = "virustotal"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        # Legacy implementation uses cursor-based pagination with limit=40 per page.
        # Keep polling until the API returns no cursor.
        findings: list[str] = []
        cursor: str | None = None

        while True:
            url = f"https://www.virustotal.com/api/v3/domains/{target}/subdomains?limit=40"
            if cursor:
                url = f"{url}&cursor={cursor}"

            try:
                data = await self.client.get_json(
                    url,
                    headers={"x-apikey": key},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 (e.g. 429 rate-limit, 403 quota) — return what we have.
                break

            for item in data.get("data", []):
                item_id = item.get("id", "")
                if item_id:
                    findings.append(item_id)

            cursor = data.get("meta", {}).get("cursor", "")
            if not cursor:
                break

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
