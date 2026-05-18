from __future__ import annotations

from urllib.parse import urlparse

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class HudsonRockResource(BaseResource):
    name = "hudsonrock"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            data = await self.client.get_json(
                "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/urls-by-domain",
                params={"domain": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()
        employees = data.get("data", {}).get("employees_urls", [])
        clients = data.get("data", {}).get("clients_urls", [])
        for record in employees + clients:
            host = urlparse(record.get("url", "")).netloc
            # Legacy filters out records containing the bullet character.
            if host and "•" not in host and host.endswith(f".{target}"):
                findings.add(host)
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
