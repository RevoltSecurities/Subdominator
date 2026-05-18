from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class OdinResource(BaseResource):
    name = "odin"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()
        # Legacy: start is None on the first call, then set from pagination.last
        start: list[str] | None = None

        while True:
            try:
                data = await self.client.request_json(
                    "POST",
                    "https://api.odin.io/v1/domain/subdomain/search",
                    headers={"X-API-Key": key, "Content-Type": "application/json"},
                    json_body={"domain": target, "limit": 1000, "start": start if start else []},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 (rate-limit / auth failure) — return what we have.
                break

            if not data.get("success"):
                break

            items = data.get("data", [])
            if not items:
                break

            findings.update(str(item) for item in items)

            # Pagination: use last cursor from response; stop when absent.
            start = data.get("pagination", {}).get("last")
            if not start:
                break

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
