from __future__ import annotations

import re

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class AbuseIpDbResource(BaseResource):
    name = "abuseipdb"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        if self.registered_domain(target) != target:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            text = await self.client.request(
                "GET",
                f"https://www.abuseipdb.com/whois/{target}",
                headers={"Cookie": "abuseipdb_session="},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [match.strip() + f".{target}" for match in re.findall(r"<li>([^<]+)</li>", text)]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
