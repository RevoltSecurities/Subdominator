from __future__ import annotations

import json
from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DnsdbResource(BaseResource):
    name = "dnsdb"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "X-API-KEY": key,
            "Accept": "application/x-ndjson",
        }

        offset_max = 0
        try:
            rate_data = await self.client.get_json(
                "https://api.dnsdb.info/dnsdb/v2/rate_limit",
                headers=headers,
            )
            rate_info = rate_data.get("rate", {})
            offset_val = str(rate_info.get("offset_max", ""))
            if offset_val and offset_val.lower() != "n/a":
                offset_max = int(offset_val)
        except Exception:
            pass

        url_base = f"https://api.dnsdb.info/dnsdb/v2/lookup/rrset/name/*.{target}?limit=0&swclient=subfinder"
        findings: set[str] = set()
        offset = 0

        while True:
            target_url = url_base
            if offset > 0:
                target_url += f"&offset={offset}"

            try:
                raw_text = await self.client.request(
                    "GET",
                    target_url,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                break

            resp_cond = ""
            for line in raw_text.splitlines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                except Exception:
                    continue

                cond = data.get("cond")
                if cond:
                    resp_cond = cond
                    
                if cond in ("", "ongoing", None):
                    obj = data.get("obj", {})
                    rrname = obj.get("rrname", "")
                    if rrname:
                        findings.add(rrname.rstrip("."))
                elif cond != "begin":
                    # Break line processing if cond marks termination markers like 'succeeded' or 'limited'
                    break

            if resp_cond == "limited":
                if offset_max != 0 and len(findings) <= offset_max:
                    offset = len(findings)
                    continue
            break

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
