from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class AnubisResource(BaseResource):
    name = "anubis"

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            data = await self.client.get_json(
                f"https://jldc.me/anubis/subdomains/{target}",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = self.normalize_findings(target, data if isinstance(data, list) else [])
        return ResourceResult(self.name, target, recursion_depth, findings)
