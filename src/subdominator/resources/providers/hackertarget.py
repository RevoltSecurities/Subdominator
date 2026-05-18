from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class HackerTargetResource(BaseResource):
    name = "hackertarget"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            text = await self.client.request(
                "GET",
                "https://api.hackertarget.com/hostsearch/",
                params={"q": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = []
        for line in text.splitlines():
            # Legacy skips the quota-exceeded message line.
            if "API count exceeded" in line:
                continue
            if "," in line:
                findings.append(line.split(",")[0])
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
