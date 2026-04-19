from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class BeVigilResource(BaseResource):
    name = "bevigil"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                f"https://osint.bevigil.com/api/{target}/subdomains",
                headers={"X-Access-Token": key},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        return ResourceResult(
            self.name, target, recursion_depth,
            self.normalize_findings(target, data.get("subdomains", [])),
        )
