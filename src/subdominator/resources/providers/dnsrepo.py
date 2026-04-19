from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DnsRepoResource(BaseResource):
    name = "dnsrepo"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        access_token, api_key = self.get_required_pair()
        if access_token is None or api_key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.get_json(
                "https://dnsarchive.net/api/",
                headers={"X-API-Access": access_token},
                params={"apikey": api_key, "search": target},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        if not isinstance(data, list):
            return ResourceResult(self.name, target, recursion_depth, [])

        # Legacy: only include entries that end with the target domain (after
        # stripping the trailing dot that the API sometimes includes).
        findings = [
            entry.get("domain", "").rstrip(".")
            for entry in data
            if isinstance(entry, dict)
            and entry.get("domain", "").rstrip(".").endswith(f".{target}")
        ]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
