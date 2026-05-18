from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RedHuntLabsResource(BaseResource):
    name = "redhuntlabs"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        # Config entry format: "https://endpoint.redhuntlabs.com/...:APIKEY"
        # from_right=True splits on the last colon so the URL (which may contain
        # colons) stays intact as the left side.
        url, key = self.get_required_pair(from_right=True)
        if url is None or key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        page = 1
        page_size = 1000
        findings: set[str] = set()

        while True:
            try:
                data = await self.client.get_json(
                    url,
                    headers={"X-BLOBR-KEY": key},
                    params={"domain": target, "page_size": str(page_size), "page": str(page)},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 — return what we have.
                break

            subdomains = data.get("subdomains", [])
            if not subdomains:
                break

            findings.update(str(item) for item in subdomains)
            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
