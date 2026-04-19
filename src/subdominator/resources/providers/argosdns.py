from __future__ import annotations

import urllib.parse
from typing import Any

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class ArgosDnsResource(BaseResource):
    name = "argosdns"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
        }
        
        findings: set[str] = set()
        page = 1
        per_page = 1000

        while True:
            endpoint = f"https://www.argosdns.io/api/v1/subdomains?domain={urllib.parse.quote(target)}&per_page={per_page}&page={page}"
            
            try:
                data = await self.client.get_json(
                    endpoint,
                    headers=headers,
                    expected_status={200},
                )
            except RuntimeError:
                break
                
            if not isinstance(data, dict):
                break

            items = data.get("data", [])
            if not isinstance(items, list) or not items:
                break

            for item in items:
                if isinstance(item, str) and item:
                    findings.add(item)
                    
            meta = data.get("meta", {})
            if not isinstance(meta, dict) or not meta.get("has_more"):
                break
                
            page += 1

        return ResourceResult(
            self.name, target, recursion_depth, self.normalize_findings(target, findings)
        )
