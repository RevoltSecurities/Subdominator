from __future__ import annotations

import asyncio
import json

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class DriftnetResource(BaseResource):
    name = "driftnet"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if not key:
            return ResourceResult(self.name, target, recursion_depth, [])

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {key}",
        }

        endpoints = [
            ("ct/log", "field=host:", "cert-dns-name"),
            ("scan/protocols", "field=host:", "cert-dns-name"),
            ("scan/domains", "field=host:", "cert-dns-name"),
            ("domain/rdns", "host=", "dns-ptr"),
        ]

        async def fetch(endpoint: str, param: str, ctx_param: str) -> dict:
            url = f"https://api.driftnet.io/v1/{endpoint}?{param}{target}&summarize=host&summary_context={ctx_param}&summary_limit=10000"
            try:
                raw_text = await self.client.request(
                    "GET",
                    url,
                    headers=headers,
                    expected_status={200, 204},
                )
                if not raw_text.strip():
                    return {}
                return json.loads(raw_text)
            except (RuntimeError, json.JSONDecodeError):
                return {}

        tasks = [fetch(ep, param, ctx) for ep, param, ctx in endpoints]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        findings: set[str] = set()

        for data in responses:
            if isinstance(data, Exception) or not isinstance(data, dict):
                continue
            
            summary = data.get("summary", {})
            if not isinstance(summary, dict):
                continue
                
            values = summary.get("values", {})
            if isinstance(values, dict):
                for subdomain in values.keys():
                    if isinstance(subdomain, str) and subdomain.endswith(f".{target}"):
                        findings.add(subdomain)

        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
