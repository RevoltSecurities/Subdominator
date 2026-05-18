from __future__ import annotations

import urllib.parse
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class OnypheResource(BaseResource):
    name = "onyphe"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        }

        page = 1
        page_size = 1000
        findings: set[str] = set()

        while True:
            q = urllib.parse.quote(f"category:resolver domain:{target}")
            url = f"https://www.onyphe.io/api/v2/search/?q={q}&page={page}&size={page_size}"

            try:
                data = await self.client.get_json(
                    url,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                break

            if not isinstance(data, dict):
                break

            results = data.get("results", [])
            if not isinstance(results, list):
                break

            for record in results:
                if not isinstance(record, dict):
                    continue

                subds = record.get("subdomains", [])
                if isinstance(subds, str):
                    findings.add(subds)
                elif isinstance(subds, list):
                    for sub in subds:
                        if isinstance(sub, str) and sub:
                            findings.add(sub)
                            
                for field in ("hostname", "forward", "reverse"):
                    val = record.get(field, "")
                    if isinstance(val, list) and val:
                        val = val[0]
                    if isinstance(val, str) and val:
                        findings.add(val)

            if len(results) == 0:
                break
                
            max_page = data.get("max_page")
            if isinstance(max_page, str) and max_page.isdigit():
                max_page = int(max_page)
                
            if isinstance(max_page, int) and page >= max_page:
                break

            page += 1

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
