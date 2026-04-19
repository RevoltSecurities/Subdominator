from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class AlienVaultResource(BaseResource):
    name = "alienvault"
    has_optional_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{target}/passive_dns"
        headers = {}
        
        # OTX Alienvault limits unauthenticated users. Using an API key prevents 429 status codes.
        key = self.provider_config.get_random_value(self.name)
        if key:
            headers["X-OTX-API-KEY"] = key

        try:
            data = await self.client.get_json(url, headers=headers if headers else None)
        except Exception:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = self.normalize_findings(
            target,
            [entry.get("hostname", "") for entry in data.get("passive_dns", [])],
        )
        return ResourceResult(self.name, target, recursion_depth, findings)