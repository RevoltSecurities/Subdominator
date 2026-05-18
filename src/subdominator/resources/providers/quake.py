from __future__ import annotations

from subdominator.core.models import ResourceResult
from subdominator.resources.base import BaseResource


class QuakeResource(BaseResource):
    name = "quake"
    requires_config = True

    async def enumerate(self, target: str, recursion_depth: int) -> ResourceResult:
        key = self.get_required_value()
        if key is None:
            return ResourceResult(self.name, target, recursion_depth, [])

        try:
            data = await self.client.request_json(
                "POST",
                "https://quake.360.net/api/v3/search/quake_service",
                headers={"X-Quaketoken": key, "Content-Type": "application/json"},
                json_body={
                    "query": f"domain: {target}",
                    "include": ["service.http.host"],
                    "latest": True,
                    "start": 0,
                    "size": 500,
                },
                expected_status={200},
            )
        except RuntimeError:
            return ResourceResult(self.name, target, recursion_depth, [])

        findings = [
            entry.get("service", {}).get("http", {}).get("host", "")
            for entry in data.get("data", [])
            if isinstance(entry, dict)
        ]
        return ResourceResult(self.name, target, recursion_depth, self.normalize_findings(target, findings))
