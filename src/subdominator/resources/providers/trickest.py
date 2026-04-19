from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class TrickestResource(BaseResource):
    name = "trickest"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {"Authorization": f"Token {key}"}
        base_url = "https://api.trickest.io/solutions/v1/public/solution/a7cba1f1-df07-4a5c-876a-953f178996be/view"
        base_params = {
            "q": f"hostname ~ '.{target}'",
            "dataset_id": "a0a49ca9-03bb-45e0-aa9a-ad59082ebdfc",
            "limit": "50",
            "select": "hostname",
            "orderby": "hostname",
        }

        # Step 1: fetch total count using offset=0.
        try:
            count_data = await self.client.get_json(
                base_url,
                headers=headers,
                params={**base_params, "offset": "0"},
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        total = int(count_data.get("total_count", 0) or 0)
        findings: set[str] = set()

        # Step 2: paginate with offset=0, 50, 100 ... until >= total.
        offset = 0
        while offset <= total:
            try:
                data = await self.client.get_json(
                    base_url,
                    headers=headers,
                    params={**base_params, "offset": str(offset)},
                    expected_status={200},
                )
            except RuntimeError:
                break

            for result in data.get("results", []):
                hostname = result.get("hostname", "")
                # Legacy: only add if hostname ends with the target domain.
                if hostname and hostname.endswith(f".{target}"):
                    findings.add(hostname)

            offset += 50

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
