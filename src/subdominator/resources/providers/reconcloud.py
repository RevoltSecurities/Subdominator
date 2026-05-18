from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ReconCloudResource(BaseResource):
    name = "reconcloud"
    requires_config = False

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        try:
            data = await self.client.get_json(
                f"https://recon.cloud/api/search?domain={target}",
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()

        if isinstance(data, dict):
            assets = data.get("cloud_assets_list", [])
            if isinstance(assets, list):
                for asset in assets:
                    if isinstance(asset, dict):
                        domain = asset.get("domain")
                        if isinstance(domain, str) and domain:
                            findings.add(domain)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
