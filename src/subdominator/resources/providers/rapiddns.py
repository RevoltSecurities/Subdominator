from __future__ import annotations

import re

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RapidDnsResource(BaseResource):
    name = "rapiddns"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            text = await self.client.request(
                "GET", 
                f"https://rapiddns.io/subdomain/{target}?full=1",
                expected_status={200}
            )
        except Exception:
            return ResourceResult(self.name, target, recursion_depth, [])

        pattern = re.compile(rf">([a-zA-Z0-9_.-]+\.{re.escape(target)})<")
        findings = pattern.findall(text)
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
