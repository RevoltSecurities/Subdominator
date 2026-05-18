from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DnsDumpsterResource(BaseResource):
    name = "dnsdumpster"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()
        page = 1

        while True:
            try:
                data = await self.client.get_json(
                    f"https://api.dnsdumpster.com/domain/{target}",
                    headers={"X-API-Key": key},
                    params={"page": str(page)},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 — return what we have.
                break

            if "error" in data:
                break

            batch = 0
            for section in ("a", "cname", "mx", "ns"):
                for record in data.get(section, []):
                    host = record.get("host", "")
                    if host and host.endswith(f".{target}"):
                        findings.add(host)
                        batch += 1

            if batch == 0:
                break

            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
