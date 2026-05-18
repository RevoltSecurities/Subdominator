from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ShrewdEyeResource(BaseResource):
    name = "shrewdeye"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            text = await self.client.request(
                "GET",
                f"https://shrewdeye.app/domains/{target}.txt",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [line.strip() for line in text.splitlines() if line.strip()]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
