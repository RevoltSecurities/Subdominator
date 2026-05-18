from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class FacebookResource(BaseResource):
    name = "facebook"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        app_id, app_secret = self.get_required_pair()
        if app_id is None or app_secret is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        access_token = f"{app_id}|{app_secret}"
        findings: set[str] = set()

        # First page uses fixed URL + params; subsequent pages use next_url
        # from the paging cursor which already contains all params embedded.
        next_url: str | None = "https://graph.facebook.com/v18.0/certificates"
        params: dict | None = {
            "fields": "domains",
            "access_token": access_token,
            "query": target,
            "limit": "1000",
        }

        while next_url is not None:
            try:
                data = await self.client.get_json(
                    next_url,
                    params=params,
                    expected_status={200},
                )
            except RuntimeError:
                break

            for item in data.get("data", []):
                findings.update(
                    domain for domain in item.get("domains", [])
                    if isinstance(domain, str)
                )

            # After the first page, params are embedded in the next URL.
            next_url = data.get("paging", {}).get("next") or None
            params = None

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
