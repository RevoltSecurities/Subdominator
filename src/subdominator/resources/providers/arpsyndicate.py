from __future__ import annotations

from urllib.parse import unquote

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ArpSyndicateResource(BaseResource):
    name = "arpsyndicate"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://api.subdomain.center/beta/",
                params={"domain": target, "auth": key},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [unquote(str(item)) for item in data if isinstance(item, str)]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
