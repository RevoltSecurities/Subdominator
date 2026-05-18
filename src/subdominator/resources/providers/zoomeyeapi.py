from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ZoomEyeApiResource(BaseResource):
    name = "zoomeyeapi"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        host, api_key = self.get_required_pair()
        if host is None or api_key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()
        page = 1

        while True:
            try:
                data = await self.client.get_json(
                    f"https://{host}/domain/search",
                    headers={
                        "API-KEY": api_key,
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    params={"q": target, "type": "1", "s": "1000", "page": str(page)},
                    expected_status={200},
                )
            except RuntimeError:
                break

            # Legacy: bail also when "list" key is absent from the response.
            if "list" not in data:
                break

            items = data.get("list", [])
            if not items:
                break

            findings.update(item.get("name", "") for item in items if isinstance(item, dict))
            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
