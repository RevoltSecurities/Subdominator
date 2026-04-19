from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class NetlasResource(BaseResource):
    name = "netlas"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        start = 0
        page_size = 20
        findings: set[str] = set()

        while True:
            try:
                data = await self.client.get_json(
                    "https://app.netlas.io/api/domains/",
                    headers={"accept": "application/json", "X-API-Key": key},
                    params={
                        "q": f"domain:*.{target} AND NOT domain:{target}",
                        "source_type": "include",
                        "start": str(start),
                    },
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 (auth failure, rate-limit) — return what we have.
                break

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                domain = item.get("data", {}).get("domain", "")
                if domain:
                    findings.add(domain)

            start += page_size

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
