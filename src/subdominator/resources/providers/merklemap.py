from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class MerkleMapResource(BaseResource):
    name = "merklemap"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        page = 0
        findings: set[str] = set()

        while True:
            try:
                data = await self.client.get_json(
                    "https://api.merklemap.com/v1/search",
                    headers={"Authorization": f"Bearer {key}"},
                    params={"query": f"*.{target}", "page": str(page), "type": "wildcard"},
                    expected_status={200},
                )
            except RuntimeError:
                # Non-200 — return what we have.
                break

            results = data.get("results", [])
            if not results:
                break

            for result in results:
                # Legacy only adds hostname/common_name if they end with the target domain.
                for field in ("hostname", "subject_common_name"):
                    value = result.get(field, "")
                    if value and value.endswith(f".{target}"):
                        findings.add(value)

            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
