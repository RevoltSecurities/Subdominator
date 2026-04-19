from __future__ import annotations

import urllib.parse

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class WhoisFreaksResource(BaseResource):
    name = "whoisfreaks"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings: set[str] = set()
        page = 1

        while True:
            endpoint = f"https://api.whoisfreaks.com/v1.0/subdomains?apiKey={key}&domain={urllib.parse.quote(target)}&status=active&page={page}"
            
            try:
                data = await self.client.get_json(
                    endpoint,
                    expected_status={200},
                )
            except RuntimeError:
                break
                
            if not isinstance(data, dict):
                break

            status = data.get("status")
            if not status:
                break

            items = data.get("subdomains", [])
            if not isinstance(items, list) or not items:
                break

            for item in items:
                if isinstance(item, dict):
                    subdomain = item.get("subdomain")
                    if isinstance(subdomain, str) and subdomain:
                        findings.add(subdomain)
                    
            current_page = data.get("current_page", 1)
            total_pages = data.get("total_pages", 1)
            
            if current_page >= total_pages:
                break
                
            page += 1

        return ResourceResult(
            self.name, target, recursion_depth, self.normalize_findings(target, findings)
        )
