from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ThcResource(BaseResource):
    name = "thc"
    requires_config = False

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        headers = {"Content-Type": "application/json"}
        api_url = "https://ip.thc.org/api/v1/lookup/subdomains"
        page_state = ""
        findings: set[str] = set()

        while True:
            req_body = {
                "domain": target,
                "page_state": page_state,
                "limit": 1000,
            }

            try:
                data = await self.client.request_json(
                    "POST",
                    api_url,
                    json_body=req_body,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                break

            if isinstance(data, dict):
                domains = data.get("domains", [])
                if isinstance(domains, list):
                    for domain_record in domains:
                        if isinstance(domain_record, dict):
                            val = domain_record.get("domain")
                            if isinstance(val, str) and val:
                                findings.add(val)
                
                # Update page state natively passing sequential variables
                next_page_state = data.get("next_page_state", "")
                if isinstance(next_page_state, str) and next_page_state:
                    page_state = next_page_state
                else:
                    break
            else:
                break

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
