from __future__ import annotations

import json
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class RobtexResource(BaseResource):
    name = "robtex"
    requires_config = False
    has_optional_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {"Content-Type": "application/x-ndjson"}
        base_url = "https://proapi.robtex.com/pdns"
        findings: set[str] = set()

        async def fetch_ndjson(url: str) -> list[dict]:
            try:
                raw_text = await self.client.request(
                    "GET",
                    url,
                    headers=headers,
                    expected_status={200},
                )
                items = []
                for line in raw_text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        items.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
                return items
            except RuntimeError:
                return []

        forward_url = f"{base_url}/forward/{target}?key={key}"
        ips = await fetch_ndjson(forward_url)

        for item in ips:
            if not isinstance(item, dict):
                continue

            rrtype = item.get("rrtype", "")
            if rrtype in ("A", "AAAA"):
                rrdata = item.get("rrdata", "")
                if not rrdata:
                    continue

                reverse_url = f"{base_url}/reverse/{rrdata}?key={key}"
                domains = await fetch_ndjson(reverse_url)
                
                for domain_item in domains:
                    if not isinstance(domain_item, dict):
                        continue
                    domain_rrdata = domain_item.get("rrdata")
                    if isinstance(domain_rrdata, str) and domain_rrdata:
                        findings.add(domain_rrdata)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
